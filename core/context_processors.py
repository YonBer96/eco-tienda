from django.conf import settings

from .utils import next_opening_message, ordering_window_open


def shop_status(request):
    return {
        'shop_open': ordering_window_open(),
        'shop_status_message': next_opening_message(),
        'APP_DISPLAY_NAME': getattr(settings, 'APP_DISPLAY_NAME', 'La Foresta Agroecológica'),
    }
