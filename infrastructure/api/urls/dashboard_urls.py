from django.urls import path
from infrastructure.api.views.dashboard_views import dashboard_view

urlpatterns = [
    path("dashboard", dashboard_view, name="dashboard"),
]