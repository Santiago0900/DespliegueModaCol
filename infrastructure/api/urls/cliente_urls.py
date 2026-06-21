from django.urls import path
from infrastructure.api.views.reporte_views import reporte_general
from infrastructure.api.views.cliente_views import (

    api_clientes,
    api_cliente_detalle,
    listar_clientes_view,
    crear_cliente_view,
    editar_cliente_view,
    guardar_cliente_view,
    eliminar_cliente_view,
    activar_cliente_view,
)

urlpatterns = [
    # API
    path("api/clientes", api_clientes, name="api_clientes"),
    path("api/clientes/<int:id>", api_cliente_detalle, name="api_cliente_detalle"),

    # HTML
    path("clientes", listar_clientes_view, name="clientes_list"),
    path("clientes/new", crear_cliente_view, name="clientes_new"),
    path("clientes/edit/<int:id>", editar_cliente_view, name="clientes_edit"),
    path("clientes/save", guardar_cliente_view, name="clientes_save"),
    path("clientes/delete/<int:id>", eliminar_cliente_view, name="clientes_delete"),
    path("clientes/activar/<int:id>", activar_cliente_view, name="clientes_activar"),
    path("reportes", reporte_general, name="reportes"),
]

