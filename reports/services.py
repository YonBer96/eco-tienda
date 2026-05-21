from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .utils import render_pdf_bytes


def _clean_recipients(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [item for item in value if item]
    return [value]


def send_customer_order_documents(pedido):
    """
    Envía automáticamente al cliente el albarán y la factura del pedido.

    Devuelve (ok, message). No lanza excepción para que confirmar un pedido no rompa
    el flujo de usuario si hay un problema SMTP/PDF.
    """
    destinatario = pedido.usuario.email or pedido.cliente.email
    if not destinatario:
        return False, 'El pedido se confirmó, pero no hay email configurado para el cliente.'

    generated_at = timezone.localtime()
    common_context = {
        'pedido': pedido,
        'generated_at': generated_at,
    }

    albaran_pdf = render_pdf_bytes('reports/albaran_individual.html', common_context)
    factura_pdf = render_pdf_bytes('reports/factura.html', common_context)

    if albaran_pdf is None or factura_pdf is None:
        return False, 'El pedido se confirmó, pero no se pudieron generar los PDFs para el email.'

    detalle_lineas = '\n'.join(
        f"- {linea.nombre_producto_snapshot}: {linea.cantidad:.2f} {linea.unidad_medida_snapshot} · {linea.total_con_iva:.2f} €"
        for linea in pedido.lineas.all()
    ) or '- Sin líneas de pedido'

    body = (
        f"Hola,\n\n"
        f"Tu pedido #{pedido.id} ha sido confirmado correctamente.\n\n"
        f"Cliente: {pedido.cliente.nombre}\n"
        f"Tienda: {pedido.tienda.nombre}\n"
        f"Ciclo: {pedido.ciclo.nombre}\n"
        f"Fecha: {generated_at.strftime('%d/%m/%Y %H:%M')}\n\n"
        f"Resumen del pedido:\n{detalle_lineas}\n\n"
        f"Base imponible: {pedido.subtotal:.2f} €\n"
        f"IVA: {pedido.total_iva:.2f} €\n"
        f"Total: {pedido.total:.2f} €\n\n"
        f"Adjuntamos el albarán y la factura en PDF.\n\n"
        f"Un saludo."
    )

    email = EmailMessage(
        subject=f'Confirmación de pedido #{pedido.id} · {pedido.cliente.nombre}',
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=_clean_recipients(destinatario),
    )
    email.attach(f'albaran_pedido_{pedido.id}.pdf', albaran_pdf, 'application/pdf')
    email.attach(f'factura_pedido_{pedido.id}.pdf', factura_pdf, 'application/pdf')

    try:
        email.send(fail_silently=False)
    except Exception as exc:
        return False, f'El pedido se confirmó, pero no se pudo enviar el email al cliente: {exc}'

    return True, f'Pedido confirmado y email enviado al cliente ({destinatario}) con albarán y factura.'
