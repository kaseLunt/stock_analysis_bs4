from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    result = float(value) * float(arg)
    return round(result, 2)

@register.filter
def in_millions(value, decimal_places=0):
    value_in_millions = float(value) / 1_000_000
    formatted_value = '{:,.{prec}f}'.format(value_in_millions, prec=decimal_places)
    return formatted_value
