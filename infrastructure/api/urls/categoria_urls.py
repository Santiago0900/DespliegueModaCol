from django.urls import path
from infrastructure.api.views.categoria_views import (
    api_categorias,
    api_categoria_detalle,
    listar_categorias_view,
    crear_categoria_view,
    editar_categoria_view,
    guardar_categoria_view,
    eliminar_categoria_view,
    activar_categoria_view,
)

urlpatterns = [
    path("api/categorias", api_categorias, name="api_categorias"),
    path("api/categorias/<int:id>", api_categoria_detalle, name="api_categoria_detalle"),

    path("categorias", listar_categorias_view, name="categorias_list"),
    path("categorias/new", crear_categoria_view, name="categorias_new"),
    path("categorias/edit/<int:id>", editar_categoria_view, name="categorias_edit"),
    path("categorias/save", guardar_categoria_view, name="categorias_save"),
    path("categorias/delete/<int:id>", eliminar_categoria_view, name="categorias_delete"),
    path("categorias/activar/<int:id>", activar_categoria_view, name="categorias_activar"),
]