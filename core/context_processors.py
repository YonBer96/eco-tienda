from django.conf import settings
from django.utils import timezone

from orders.models import OrderCycle


def shop_status(request):
    now = timezone.now()

    ciclo = OrderCycle.objects.filter(
        cerrado=False,
        inicio__lte=now,
        cierre__gte=now
    ).order_by('-inicio').first()

    if ciclo:
        shop_open = True
        shop_status_message = f'La tienda está abierta para la semana {ciclo.nombre} hasta {ciclo.cierre.strftime("%d/%m/%Y %H:%M")}.'
    else:
        shop_open = False
        proximo = OrderCycle.objects.filter(
            cerrado=False,
            inicio__gt=now
        ).order_by('inicio').first()

        if proximo:
            shop_status_message = f'La tienda está cerrada. Próxima apertura: {proximo.inicio.strftime("%d/%m/%Y %H:%M")}.'
        else:
            shop_status_message = 'La tienda está cerrada. No hay ningún ciclo de pedidos activo.'

    return {
        'shop_open': shop_open,
        'shop_status_message': shop_status_message,
        'APP_DISPLAY_NAME': getattr(settings, 'APP_DISPLAY_NAME', 'La Foresta Agroecológica'),
    }