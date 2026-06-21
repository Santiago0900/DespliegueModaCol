from django.urls import path
from infrastructure.api.views.rol_views import (
    api_roles,
    api_rol_detalle,
    listar_roles_view,
    crear_rol_view,
    editar_rol_view,
    guardar_rol_view,
    eliminar_rol_view,
    activar_rol_view,
)

urlpatterns = [
    path("api/roles", api_roles, name="api_roles"),
    path("api/roles/<int:id>", api_rol_detalle, name="api_rol_detalle"),

    path("roles", listar_roles_view, name="roles_list"),
    path("roles/new", crear_rol_view, name="roles_new"),
    path("roles/edit/<int:id>", editar_rol_view, name="roles_edit"),
    path("roles/save", guardar_rol_view, name="roles_save"),
    path("roles/delete/<int:id>", eliminar_rol_view, name="roles_delete"),
    path("roles/activar/<int:id>", activar_rol_view, name="roles_activar"),
]