from django.urls import path
from infrastructure.api.views.proveedor_views import (
    api_proveedores,
    api_proveedor_detalle,
    listar_proveedores_view,
    crear_proveedor_view,
    editar_proveedor_view,
    guardar_proveedor_view,
    eliminar_proveedor_view,
    activar_proveedor_view,
)

urlpatterns = [
    path("api/proveedores", api_proveedores, name="api_proveedores"),
    path("api/proveedores/<int:id>", api_proveedor_detalle, name="api_proveedor_detalle"),

    path("proveedores", listar_proveedores_view, name="proveedores_list"),
    path("proveedores/new", crear_proveedor_view, name="proveedores_new"),
    path("proveedores/edit/<int:id>", editar_proveedor_view, name="proveedores_edit"),
    path("proveedores/save", guardar_proveedor_view, name="proveedores_save"),
    path("proveedores/delete/<int:id>", eliminar_proveedor_view, name="proveedores_delete"),
    path("proveedores/activar/<int:id>", activar_proveedor_view, name="proveedores_activar"),
]