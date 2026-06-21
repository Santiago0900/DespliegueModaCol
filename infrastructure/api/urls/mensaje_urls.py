from django.urls import path
from infrastructure.api.views.mensaje_views import *

urlpatterns = [
    path("mensajes", mensajes_view),
    path("mensajes/enviar", enviar_mensaje_view),
    path("mensajes/marcar-leido/<int:id>", marcar_leido_view),
]