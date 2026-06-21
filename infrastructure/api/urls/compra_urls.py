from django.urls import path
from infrastructure.api.views.compra_views import (
    api_compras,
    api_compra_detalle,
    listar_compras_view,
    crear_compra_view,
    editar_compra_view,
    guardar_compra_view,
    eliminar_compra_view,
    activar_compra_view,
)

urlpatterns = [
    path("api/compras", api_compras, name="api_compras"),
    path("api/compras/<int:id>", api_compra_detalle, name="api_compra_detalle"),

    path("compras", listar_compras_view, name="compras_list"),
    path("compras/new", crear_compra_view, name="compras_new"),
    path("compras/edit/<int:id>", editar_compra_view, name="compras_edit"),
    path("compras/save", guardar_compra_view, name="compras_save"),
    path("compras/delete/<int:id>", eliminar_compra_view, name="compras_delete"),
    path("compras/activar/<int:id>", activar_compra_view, name="compras_activar"),

]
