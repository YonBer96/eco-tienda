from datetime import datetime, time, timedelta

from django.utils import timezone

SHOP_OPEN_WEEKDAY = 3  # jueves
SHOP_OPEN_TIME = time(14, 0)
SHOP_CLOSE_WEEKDAY = 5  # sábado
SHOP_CLOSE_TIME = time(20, 0)

WEEKDAYS_ES = {
    0: 'lunes',
    1: 'martes',
    2: 'miércoles',
    3: 'jueves',
    4: 'viernes',
    5: 'sábado',
    6: 'domingo',
}


def _current_open_window(now=None):
    now = now or timezone.localtime()
    weekday = now.weekday()

    if weekday < SHOP_OPEN_WEEKDAY or weekday > SHOP_CLOSE_WEEKDAY:
        return False
    if weekday == SHOP_OPEN_WEEKDAY and now.time() < SHOP_OPEN_TIME:
        return False
    if weekday == SHOP_CLOSE_WEEKDAY and now.time() >= SHOP_CLOSE_TIME:
        return False
    return True


def ordering_window_open(now=None):
    return _current_open_window(now)


def next_opening_message(now=None):
    now = now or timezone.localtime()
    if ordering_window_open(now):
        return 'La tienda está abierta para pedidos y modificaciones hasta el sábado a las 20:00.'

    weekday = now.weekday()
    days_until_thursday = (SHOP_OPEN_WEEKDAY - weekday) % 7
    next_open_date = now.date() + timedelta(days=days_until_thursday)
    next_open = datetime.combine(next_open_date, SHOP_OPEN_TIME)
    next_open = timezone.make_aware(next_open, timezone.get_current_timezone())
    if days_until_thursday == 0 and now.time() < SHOP_OPEN_TIME:
        return f'La tienda abrirá hoy a las {SHOP_OPEN_TIME:%H:%M}.'
    weekday_es = WEEKDAYS_ES[next_open.weekday()]
    return f'La tienda abrirá el {weekday_es} {next_open:%d/%m} a las {next_open:%H:%M}.'


def current_week_label(now=None):
    now = now or timezone.localtime()
    year, week, _ = now.isocalendar()
    return f'Semana {week}-{year}'
