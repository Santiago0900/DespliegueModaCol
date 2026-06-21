from django.urls import path
from infrastructure.api.views.producto_views import (
    api_productos,
    api_producto_detalle,
    listar_productos_view,
    crear_producto_view,
    editar_producto_view,
    guardar_producto_view,
    eliminar_producto_view,
    activar_producto_view,
)

urlpatterns = [
    path("api/productos", api_productos, name="api_productos"),
    path("api/productos/<int:id>", api_producto_detalle, name="api_producto_detalle"),

    path("", listar_productos_view, name="productos_list"),
    path("new", crear_producto_view, name="productos_new"),
    path("edit/<int:id>", editar_producto_view, name="productos_edit"),
    path("save", guardar_producto_view, name="productos_save"),
    path("delete/<int:id>", eliminar_producto_view, name="productos_delete"),
    path("activar/<int:id>", activar_producto_view, name="productos_activar"),
]