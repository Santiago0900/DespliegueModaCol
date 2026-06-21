from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("infrastructure.api.urls.auth_urls")),
    path("", include("infrastructure.api.urls.dashboard_urls")),
    path("", include("infrastructure.api.urls.cliente_urls")),
    path("", include("infrastructure.api.urls.categoria_urls")),
    path("usuarios/", include("infrastructure.api.urls.usuario_urls")),
    path("productos/", include("infrastructure.api.urls.producto_urls")),
    path("", include("infrastructure.api.urls.proveedor_urls")),
    path("", include("infrastructure.api.urls.compra_urls")),
    path("", include("infrastructure.api.urls.flujo_caja_urls")),
    path("", include("infrastructure.api.urls.rol_urls")),
    path("", include("infrastructure.api.urls.venta_urls")),
    path("", include("infrastructure.api.urls.mensaje_urls")),
]
