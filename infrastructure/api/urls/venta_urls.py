from django.urls import path
from infrastructure.api.views.venta_views import (
    api_ventas,
    api_venta_detalle,
    listar_ventas_view,
    crear_venta_view,
    editar_venta_view,
    guardar_venta_view,
    eliminar_venta_view,
    activar_venta_view,
)

urlpatterns = [
    path("api/ventas", api_ventas, name="api_ventas"),
    path("api/ventas/<int:id>", api_venta_detalle, name="api_venta_detalle"),

    path("ventas", listar_ventas_view, name="ventas_list"),
    path("ventas/new", crear_venta_view, name="ventas_new"),
    path("ventas/edit/<int:id>", editar_venta_view, name="ventas_edit"),
    path("ventas/save", guardar_venta_view, name="ventas_save"),
    path("ventas/delete/<int:id>", eliminar_venta_view, name="ventas_delete"),
    path("ventas/activar/<int:id>", activar_venta_view, name="ventas_activar"),
]