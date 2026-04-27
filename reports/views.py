from collections import defaultdict
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Producto, Proveedor
from orders.models import LineaPedido, OrderCycle, Pedido
from .forms import EmailDraftForm
from .utils import render_pdf
from django.core.mail import EmailMessage
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def quantize_2(value):
    if value is None:
        return Decimal('0.00')
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def _build_box_breakdown(total_cantidad, formato_caja):
    total_cantidad = quantize_2(total_cantidad)
    if not formato_caja or formato_caja <= 0:
        return {
            'formato_caja': None,
            'cajas_completas': None,
            'resto_suelto': None,
            'pedido_proveedor': 'Sin formato de caja',
        }

    cajas = int((total_cantidad / formato_caja).to_integral_value(rounding=ROUND_DOWN))
    resto = quantize_2(total_cantidad - (formato_caja * cajas))
    pedido_proveedor = f'{cajas} caja(s)' if resto <= 0 else f'{cajas} caja(s) + {resto:.2f}'

    return {
        'formato_caja': quantize_2(formato_caja),
        'cajas_completas': cajas,
        'resto_suelto': resto,
        'pedido_proveedor': pedido_proveedor,
    }


def get_latest_cycle():
    return OrderCycle.objects.order_by('-inicio').first()


def get_cycle_or_latest(ciclo_id=None):
    if ciclo_id:
        return get_object_or_404(OrderCycle, pk=ciclo_id)
    return get_latest_cycle()


def _product_box_formats():
    return {item['nombre']: item['formato_caja'] for item in Producto.objects.values('nombre', 'formato_caja')}


def build_weekly_summary(ciclo):
    formatos = _product_box_formats()
    resumen = list(
        LineaPedido.objects
        .filter(pedido__ciclo=ciclo, pedido__estado=Pedido.CONFIRMADO)
        .values('nombre_producto_snapshot', 'unidad_medida_snapshot')
        .annotate(total_cantidad=Sum('cantidad'))
        .order_by('nombre_producto_snapshot')
    )
    for item in resumen:
        item['total_cantidad'] = quantize_2(item['total_cantidad'])
        item.update(_build_box_breakdown(item['total_cantidad'], formatos.get(item['nombre_producto_snapshot'])))
    total_referencias = len(resumen)
    total_cantidad = quantize_2(sum((item['total_cantidad'] or Decimal('0.00')) for item in resumen))
    return {
        'lineas': resumen,
        'total_referencias': total_referencias,
        'total_cantidad': total_cantidad,
    }


def build_supplier_summary(ciclo):
    formatos = _product_box_formats()
    lineas = list(
        LineaPedido.objects
        .filter(pedido__ciclo=ciclo, pedido__estado=Pedido.CONFIRMADO)
        .values(
            'proveedor_snapshot',
            'proveedor_snapshot__nombre',
            'proveedor_snapshot__email',
            'proveedor_snapshot__contacto',
            'nombre_producto_snapshot',
            'unidad_medida_snapshot',
        )
        .annotate(total_cantidad=Sum('cantidad'))
        .order_by('proveedor_snapshot__nombre', 'nombre_producto_snapshot')
    )

    grouped = defaultdict(list)
    supplier_totals = {}
    suppliers = []
    seen_supplier_ids = set()

    for item in lineas:
        item['total_cantidad'] = quantize_2(item['total_cantidad'])
        item.update(_build_box_breakdown(item['total_cantidad'], formatos.get(item['nombre_producto_snapshot'])))
        proveedor_id = item['proveedor_snapshot']
        grouped[proveedor_id].append(item)
        supplier_totals.setdefault(proveedor_id, Decimal('0.00'))
        supplier_totals[proveedor_id] = quantize_2(supplier_totals[proveedor_id] + (item['total_cantidad'] or Decimal('0.00')))
        if proveedor_id not in seen_supplier_ids:
            suppliers.append({
                'id': proveedor_id,
                'nombre': item['proveedor_snapshot__nombre'],
                'email': item['proveedor_snapshot__email'],
                'contacto': item['proveedor_snapshot__contacto'],
                'lineas': grouped[proveedor_id],
            })
            seen_supplier_ids.add(proveedor_id)

    for supplier in suppliers:
        supplier['total'] = supplier_totals.get(supplier['id'], Decimal('0.00'))

    return {
        'suppliers': suppliers,
        'grouped': dict(grouped),
        'flat': lineas,
        'supplier_totals': supplier_totals,
        'supplier_count': len(suppliers),
    }


def _is_real_email_backend():
    backend = getattr(settings, 'EMAIL_BACKEND', '') or ''
    host = getattr(settings, 'EMAIL_HOST', '') or ''
    user = getattr(settings, 'EMAIL_HOST_USER', '') or ''
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', '') or ''
    return backend != 'django.core.mail.backends.console.EmailBackend' and bool(host and user and password)


def _email_setup_warning():
    if _is_real_email_backend():
        return ''
    return 'El borrador funciona correctamente. Para que el envío sea real revisa la configuración SMTP del archivo .env.'


def _pedido_email_initial(pedido):
    destinatario = pedido.usuario.email or pedido.cliente.email
    detalle_lineas = '\n'.join(
        f"- {linea.nombre_producto_snapshot}: {linea.cantidad:.2f} {linea.unidad_medida_snapshot} · {linea.total_con_iva:.2f} €"
        for linea in pedido.lineas.all()
    ) or '- Sin líneas de pedido'
    body = (
        f"Hola,\n\n"
        f"Te envío el detalle del pedido #{pedido.id} correspondiente a {pedido.cliente.nombre}.\n\n"
        f"Tienda: {pedido.tienda.nombre}\n"
        f"Fecha: {timezone.localtime().strftime('%d/%m/%Y %H:%M')}\n\n"
        f"Detalle del pedido:\n{detalle_lineas}\n\n"
        f"Base imponible: {pedido.subtotal:.2f} €\n"
        f"IVA: {pedido.total_iva:.2f} €\n"
        f"Total: {pedido.total:.2f} €\n\n"
        f"Quedo a tu disposición para cualquier aclaración.\n\n"
        f"Un saludo."
    )
    return {
        'to': destinatario,
        'subject': f'Albarán pedido #{pedido.id} · {pedido.cliente.nombre}',
        'body': body,
    }


def _supplier_email_initial(ciclo, proveedor):
    lineas = list(
        LineaPedido.objects
        .filter(pedido__ciclo=ciclo, pedido__estado=Pedido.CONFIRMADO, proveedor_snapshot=proveedor)
        .values('nombre_producto_snapshot', 'unidad_medida_snapshot')
        .annotate(total_cantidad=Sum('cantidad'))
        .order_by('nombre_producto_snapshot')
    )
    formatos = _product_box_formats()
    detalle = []
    for item in lineas:
        item['total_cantidad'] = quantize_2(item['total_cantidad'])
        item.update(_build_box_breakdown(item['total_cantidad'], formatos.get(item['nombre_producto_snapshot'])))
        detalle.append(
            f"- {item['nombre_producto_snapshot']}: {item['total_cantidad']:.2f} {item['unidad_medida_snapshot']}"
            + (f" · Pedido: {item['pedido_proveedor']}" if item['pedido_proveedor'] else '')
        )
    detalle_lineas = '\n'.join(detalle) or '- Sin líneas de pedido'
    body = (
        f"Hola {proveedor.contacto or proveedor.nombre},\n\n"
        f"Me gustaría realizar el siguiente pedido correspondiente al ciclo {ciclo.nombre}.\n\n"
        f"Detalle:\n{detalle_lineas}\n\n"
        f"Por favor, confirmad disponibilidad y plazo de entrega cuando os sea posible.\n\n"
        f"Muchas gracias.\n"
    )
    return {
        'to': proveedor.email,
        'subject': f'Pedido semanal · {ciclo.nombre} · {proveedor.nombre}',
        'body': body,
        'lineas': lineas,
    }


@login_required
def albaran_individual_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente', 'tienda', 'usuario').prefetch_related('lineas__proveedor_snapshot'), pk=pedido_id)

    if not request.user.is_superuser and pedido.usuario_id != request.user.id:
        raise Http404()

    response = render_pdf(
        'reports/albaran_individual.html',
        {'pedido': pedido, 'generated_at': timezone.localtime()},
        filename=f'albaran_pedido_{pedido.id}.pdf'
    )

    if response is None:
        messages.error(request, 'La generación de PDF no está disponible porque WeasyPrint no está instalado correctamente en este equipo.')
        return redirect('pedido_detail', pk=pedido.id)

    return response


@login_required
def factura_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente', 'tienda', 'usuario').prefetch_related('lineas__proveedor_snapshot'), pk=pedido_id)

    if not request.user.is_superuser and pedido.usuario_id != request.user.id:
        raise Http404()

    response = render_pdf(
        'reports/factura.html',
        {'pedido': pedido, 'generated_at': timezone.localtime()},
        filename=f'factura_pedido_{pedido.id}.pdf'
    )

    if response is None:
        messages.error(request, 'La generación de PDF no está disponible porque WeasyPrint no está instalado correctamente en este equipo.')
        return redirect('pedido_detail', pk=pedido.id)

    return response

@login_required
def enviar_albaran_email(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente', 'tienda', 'usuario').prefetch_related('lineas'),
        pk=pedido_id
    )

    if not request.user.is_superuser and pedido.usuario_id != request.user.id:
        raise Http404()

    initial = _pedido_email_initial(pedido)

    if not initial['to']:
        messages.error(request, 'No hay un correo configurado para este pedido o usuario.')
        return redirect('pedido_detail', pk=pedido.id)

    if request.method == 'POST':
        form = EmailDraftForm(request.POST)

        if form.is_valid():
            attach_pdf = request.POST.get('attach_pdf') == 'on'

            email = EmailMessage(
                subject=form.cleaned_data['subject'],
                body=form.cleaned_data['body'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[form.cleaned_data['to']],
                cc=[x.strip() for x in form.cleaned_data['cc'].split(',') if x.strip()],
            )

            if attach_pdf:
                try:
                    pdf_response = albaran_individual_pdf(request, pedido.id)
                    email.attach(
                        f'albaran_pedido_{pedido.id}.pdf',
                        pdf_response.content,
                        'application/pdf'
                    )
                except Exception as exc:
                    messages.error(request, f'No se pudo generar el PDF del albarán: {exc}')
                    return redirect('pedido_detail', pk=pedido.id)

            try:
                email.send(fail_silently=False)
            except Exception as exc:
                messages.error(request, f'No se pudo enviar el correo: {exc}')
            else:
                extra = '' if _is_real_email_backend() else ' El proyecto está en modo consola; para envío real configura SMTP.'
                if attach_pdf:
                    messages.success(
                        request,
                        f'Correo enviado correctamente a {form.cleaned_data["to"]} con el PDF adjunto.{extra}'
                    )
                else:
                    messages.success(
                        request,
                        f'Correo enviado correctamente a {form.cleaned_data["to"]} sin PDF adjunto.{extra}'
                    )
                return redirect('pedido_detail', pk=pedido.id)
    else:
        form = EmailDraftForm(initial=initial)

    return render(request, 'reports/email_draft.html', {
        'form': form,
        'title': f'Preparar correo del pedido #{pedido.id}',
        'subtitle': f'{pedido.cliente.nombre} · {pedido.tienda.nombre}',
        'back_url': 'pedido_detail',
        'back_id': pedido.id,
        'summary_title': 'Resumen del pedido',
        'summary_lines': [
            f'{linea.nombre_producto_snapshot} · {linea.cantidad:.2f} {linea.unidad_medida_snapshot} · {linea.total_con_iva:.2f} €'
            for linea in pedido.lineas.all()
        ],
        'warning': _email_setup_warning(),
        'send_label': 'Enviar correo',
    })


@user_passes_test(lambda u: u.is_superuser)
def supplier_email_draft(request, proveedor_id):
    ciclo = get_cycle_or_latest(request.GET.get('ciclo_id'))
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if not ciclo:
        messages.error(request, 'No hay ciclos disponibles.')
        return redirect('supplier_summary')

    initial = _supplier_email_initial(ciclo, proveedor)

    if not initial['to']:
        messages.error(request, 'El proveedor no tiene un correo configurado.')
        return redirect('supplier_summary')

    if request.method == 'POST':
        form = EmailDraftForm(request.POST)

        if form.is_valid():
            attach_pdf = request.POST.get('attach_pdf') == 'on'

            email = EmailMessage(
                subject=form.cleaned_data['subject'],
                body=form.cleaned_data['body'],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[form.cleaned_data['to']],
                cc=[x.strip() for x in form.cleaned_data['cc'].split(',') if x.strip()],
            )

            if attach_pdf:
                try:
                    pdf_response = supplier_single_pdf(request, proveedor.id, ciclo.id)

                    if not pdf_response.content:
                        messages.error(request, 'El PDF del albarán se generó vacío.')
                        return redirect('supplier_summary')

                    email.attach(
                        filename=f'albaran_proveedor_{proveedor.nombre}.pdf',
                        content=pdf_response.content,
                        mimetype='application/pdf',
                    )

                except Exception as exc:
                    messages.error(request, f'No se pudo adjuntar el PDF del albarán: {exc}')
                    return redirect('supplier_summary')

            try:
                email.send(fail_silently=False)
            except Exception as exc:
                messages.error(request, f'No se pudo enviar el correo: {exc}')
            else:
                extra = '' if _is_real_email_backend() else ' El proyecto está en modo consola; para envío real configura SMTP.'

                if attach_pdf:
                    messages.success(
                        request,
                        f'Correo al proveedor enviado a {form.cleaned_data["to"]} con PDF adjunto.{extra}'
                    )
                else:
                    messages.success(
                        request,
                        f'Correo al proveedor enviado a {form.cleaned_data["to"]} sin PDF adjunto.{extra}'
                    )

                return redirect('supplier_summary')
    else:
        form = EmailDraftForm(initial=initial)

    return render(request, 'reports/email_draft.html', {
        'form': form,
        'title': f'Preparar correo a proveedor · {proveedor.nombre}',
        'subtitle': ciclo.nombre,
        'back_url': 'supplier_summary',
        'summary_title': 'Líneas agrupadas del proveedor',
        'summary_lines': [
            f"{item['nombre_producto_snapshot']} · {item['total_cantidad']:.2f} {item['unidad_medida_snapshot']} · {item['pedido_proveedor']}"
            for item in initial['lineas']
        ],
        'warning': _email_setup_warning(),
        'send_label': 'Enviar correo al proveedor',
    })


@user_passes_test(lambda u: u.is_superuser)
def weekly_summary(request):
    ciclo = get_cycle_or_latest()
    resumen = build_weekly_summary(ciclo) if ciclo else {'lineas': [], 'total_referencias': 0, 'total_cantidad': Decimal('0.00')}
    return render(request, 'reports/weekly_summary.html', {'ciclo': ciclo, 'resumen': resumen})


@user_passes_test(lambda u: u.is_superuser)
def supplier_summary(request):
    ciclo = get_cycle_or_latest()
    proveedor_data = build_supplier_summary(ciclo) if ciclo else {'suppliers': [], 'grouped': {}, 'supplier_totals': {}, 'supplier_count': 0, 'flat': []}
    return render(request, 'reports/supplier_summary.html', {'ciclo': ciclo, **proveedor_data})


@user_passes_test(lambda u: u.is_superuser)
def weekly_summary_pdf(request, ciclo_id=None):
    ciclo = get_cycle_or_latest(ciclo_id)
    if not ciclo:
        messages.error(request, 'No hay ciclos disponibles.')
        return redirect('admin_dashboard')

    resumen = build_weekly_summary(ciclo)
    response = render_pdf(
        'reports/albaran_general.html',
        {'ciclo': ciclo, 'resumen': resumen, 'generated_at': timezone.localtime()},
        filename=f'albaran_general_ciclo_{ciclo.id}.pdf'
    )
    if response is None:
        messages.error(request, 'La generación de PDF no está disponible porque WeasyPrint no está instalado correctamente en este equipo.')
        return redirect('weekly_summary')
    return response


@user_passes_test(lambda u: u.is_superuser)
def supplier_summary_pdf(request, ciclo_id=None):
    ciclo = get_cycle_or_latest(ciclo_id)
    if not ciclo:
        messages.error(request, 'No hay ciclos disponibles.')
        return redirect('admin_dashboard')

    proveedor_data = build_supplier_summary(ciclo)
    response = render_pdf(
        'reports/albaran_proveedores.html',
        {'ciclo': ciclo, **proveedor_data, 'generated_at': timezone.localtime()},
        filename=f'albaran_proveedores_ciclo_{ciclo.id}.pdf'
    )
    if response is None:
        messages.error(request, 'La generación de PDF no está disponible porque WeasyPrint no está instalado correctamente en este equipo.')
        return redirect('supplier_summary')
    return response


@user_passes_test(lambda u: u.is_superuser)
def albaran_semanal_general_pdf(request, ciclo_id):
    return weekly_summary_pdf(request, ciclo_id=ciclo_id)


@user_passes_test(lambda u: u.is_superuser)
def albaran_por_proveedor_pdf(request, ciclo_id):
    return supplier_summary_pdf(request, ciclo_id=ciclo_id)

@user_passes_test(lambda u: u.is_superuser)
def supplier_single_pdf(request, proveedor_id, ciclo_id=None):
    ciclo = get_cycle_or_latest(ciclo_id)
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if not ciclo:
        messages.error(request, 'No hay ciclos disponibles.')
        return redirect('supplier_summary')

    proveedor_data = build_supplier_summary(ciclo)

    suppliers = [
        s for s in proveedor_data['suppliers']
        if s['id'] == proveedor.id
    ]

    response = render_pdf(
        'reports/albaran_proveedores.html',
        {
            'ciclo': ciclo,
            **proveedor_data,
            'suppliers': suppliers,
            'supplier_count': len(suppliers),
            'generated_at': timezone.localtime(),
        },
        filename=f'albaran_{proveedor.nombre}_ciclo_{ciclo.id}.pdf'
    )

    if response is None:
        messages.error(request, 'La generación de PDF no está disponible.')
        return redirect('supplier_summary')

    return response