from django.urls import path
from infrastructure.api.views.flujo_caja_views import listar_flujo_caja_view

urlpatterns = [
    path("flujo-caja", listar_flujo_caja_view, name="flujo_caja_list"),
]