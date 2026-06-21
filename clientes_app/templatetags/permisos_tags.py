from django import template

register = template.Library()

@register.simple_tag
def tiene_permiso(user, modulo, accion):
    return user.tiene_permiso(modulo, accion)