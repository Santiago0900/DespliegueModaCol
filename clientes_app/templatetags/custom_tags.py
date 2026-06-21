from django import template

register = template.Library()

# Este es el que te falta para el formulario de Roles
@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    # Como key suele ser el ID del módulo (int), aseguramos que funcione
    return dictionary.get(key)

# Este es el que ya tenías
@register.filter
def tiene_permiso(user, permiso):
    try:
        modulo, accion = permiso.split(",")
        return user.tiene_permiso(modulo, accion)
    except:
        return False