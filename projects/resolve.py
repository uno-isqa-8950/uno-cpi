from django import template
from django.template.base import Variable, VariableDoesNotExist

register = template.Library()


@register.simple_tag
def resolve(lookup, target):
    try:
        return lookup[target]
    except VariableDoesNotExist:
        return None