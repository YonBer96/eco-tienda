from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Cliente
from catalog.models import CategoriaProducto, Producto
from core.utils import ordering_window_open

from .forms import PedidoMetaForm
from .models import LineaPedido, OrderCycle, Pedido


def get_current_cycle():
    return OrderCycle.objects.filter(cerrado=False).order_by('-inicio').first()


def quantize_2(value):
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@login_required
def pedido_list(request):
    pedidos = Pedido.objects.select_related('cliente', 'tienda', 'usuario', 'ciclo')
    if not request.user.is_superuser:
        pedidos = pedidos.filter(usuario=request.user)
    return render(request, 'orders/pedido_list.html', {'pedidos': pedidos})


@login_required
@transaction.atomic
def pedido_create(request):
    ciclo = get_current_cycle()
    if not ciclo or not ciclo.esta_abierto or (not request.user.is_superuser and not ordering_window_open()):
        messages.error(request, 'La tienda está cerrada en este momento.')
        return redirect('pedido_list')

    if request.method == 'POST':
        form = PedidoMetaForm(request.POST, user=request.user)
        if form.is_valid():
            tienda = form.cleaned_data['tienda']
            cliente = form.cleaned_data['cliente']
            try:
                pedido, created = Pedido.objects.get_or_create(
                    ciclo=ciclo,
                    tienda=tienda,
                    defaults={
                        'usuario': request.user,
                        'cliente': cliente,
                        'observaciones': form.cleaned_data.get('observaciones', ''),
                    }
                )
                if not created:
                    if not pedido.puede_editarse_por(request.user):
                        raise Http404
                    messages.info(request, 'Ya existía un pedido para esa tienda esta semana. Se ha abierto para editarlo.')
                else:
                    pedido.observaciones = form.cleaned_data.get('observaciones', '')
                    pedido.save()
            except IntegrityError:
                messages.error(request, 'No se pudo crear el pedido.')
                return redirect('pedido_list')
            return redirect('pedido_edit', pk=pedido.pk)
    else:
        initial = {}
        if not request.user.is_superuser:
            primer_cliente = Cliente.objects.filter(usuarios=request.user, activo=True).first()
            if primer_cliente:
                initial['cliente'] = primer_cliente
        form = PedidoMetaForm(user=request.user, initial=initial)

    return render(request, 'orders/pedido_form.html', {'form': form, 'ciclo': ciclo})


@login_required
@transaction.atomic
def pedido_edit(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related('ciclo', 'cliente', 'tienda'), pk=pk)
    if not pedido.puede_editarse_por(request.user):
        raise Http404('No tienes permiso para editar este pedido.')

    productos = Producto.objects.filter(activo=True).select_related('categoria', 'proveedor').order_by('nombre')
    categorias = list(CategoriaProducto.ordered_queryset())

    if request.method == 'POST':
        pedido.observaciones = request.POST.get('observaciones', '').strip()
        pedido.save(update_fields=['observaciones', 'actualizado_en'])

        for producto in productos:
            raw_qty = request.POST.get(f'producto_{producto.id}', '').strip().replace(',', '.')
            try:
                cantidad = Decimal(raw_qty) if raw_qty else Decimal('0.00')
            except InvalidOperation:
                cantidad = Decimal('0.00')

            cantidad = quantize_2(cantidad)

            linea, created = LineaPedido.objects.get_or_create(
                pedido=pedido,
                producto=producto,
                defaults={
                    'proveedor_snapshot': producto.proveedor,
                    'nombre_producto_snapshot': producto.nombre,
                    'unidad_medida_snapshot': producto.unidad_medida,
                    'precio_unitario_snapshot': producto.precio,
                    'iva_snapshot': producto.iva,
                    'cantidad': Decimal('0.00'),
                }
            )

            if cantidad <= 0:
                if not created:
                    linea.delete()
                continue

            if producto.pedido_minimo and cantidad < producto.pedido_minimo:
                cantidad = producto.pedido_minimo

            if producto.incremento_pedido and producto.incremento_pedido > 0:
                pasos = (cantidad / producto.incremento_pedido).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                cantidad = quantize_2(pasos * producto.incremento_pedido)

            if producto.limitar_stock and producto.stock_disponible and cantidad > producto.stock_disponible:
                cantidad = producto.stock_disponible

            linea.proveedor_snapshot = producto.proveedor
            linea.nombre_producto_snapshot = producto.nombre
            linea.unidad_medida_snapshot = producto.unidad_medida
            linea.precio_unitario_snapshot = producto.precio
            linea.iva_snapshot = producto.iva
            linea.cantidad = cantidad
            linea.save()

        if 'confirmar' in request.POST:
            pedido.estado = Pedido.CONFIRMADO
            pedido.save(update_fields=['estado', 'actualizado_en'])
            messages.success(request, 'Pedido confirmado correctamente.')
            return redirect('pedido_detail', pk=pedido.pk)

        messages.success(request, 'Pedido actualizado correctamente.')
        return redirect('pedido_edit', pk=pedido.pk)

    lineas_map = {linea.producto_id: linea for linea in pedido.lineas.all()}

    return render(request, 'orders/pedido_edit.html', {
        'pedido': pedido,
        'productos': productos,
        'categorias': categorias,
        'lineas_map': lineas_map,
    })


@login_required
def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente', 'tienda', 'usuario', 'ciclo').prefetch_related('lineas__proveedor_snapshot'),
        pk=pk,
    )
    if not request.user.is_superuser and pedido.usuario_id != request.user.id:
        raise Http404
    return render(request, 'orders/pedido_detail.html', {'pedido': pedido})


@login_required
@transaction.atomic
def pedido_delete(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if not pedido.puede_editarse_por(request.user):
        raise Http404

    if request.method == 'POST':
        pedido.estado = Pedido.ANULADO
        pedido.save(update_fields=['estado', 'actualizado_en'])
        messages.warning(request, 'Pedido anulado correctamente.')
        return redirect('pedido_list')

    return render(request, 'orders/pedido_confirm_delete.html', {'pedido': pedido})
