from decimal import Decimal, ROUND_HALF_UP

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def money(value):
    if value in (None, ''):
        value = Decimal('0.00')
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


@register.filter
def qty2(value):
    return money(value)


@register.filter
def can_edit(pedido, user):
    return pedido.puede_editarse_por(user)
