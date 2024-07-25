from django import template

register = template.Library()

@register.filter
def split_price(value):
    try:
        integer_part, decimal_part = f"{value:.2f}".split('.')
    except ValueError:
        integer_part, decimal_part = str(value), '00'
    return {'integer':integer_part, 'decimal':decimal_part}