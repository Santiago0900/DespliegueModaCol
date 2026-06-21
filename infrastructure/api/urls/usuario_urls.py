from django.urls import path
from infrastructure.api.views.usuario_views import (
    api_usuarios,
    api_usuario_detalle,
    listar_usuarios_view,
    crear_usuario_view,
    editar_usuario_view,
    guardar_usuario_view,
    eliminar_usuario_view,
    activar_usuario_view,
    set_password_view,
)

urlpatterns = [
    path("api/usuarios", api_usuarios, name="api_usuarios"),
    path("api/usuarios/<int:id>", api_usuario_detalle, name="api_usuario_detalle"),

    path("", listar_usuarios_view, name="usuarios_list"),
    path("new", crear_usuario_view, name="usuarios_new"),
    path("edit/<int:id>", editar_usuario_view, name="usuarios_edit"),
    path("save", guardar_usuario_view, name="usuarios_save"),
    path("delete/<int:id>", eliminar_usuario_view, name="usuarios_delete"),
    path("activar/<int:id>", activar_usuario_view, name="usuarios_activar"),
    path("set-password/<str:token>", set_password_view, name="set_password"),
]
