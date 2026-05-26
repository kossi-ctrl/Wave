from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # JSON endpoints for charts
    path("api/line-bar/", views.api_line_bar, name="api_line_bar"),
    path("api/scatter/", views.api_scatter, name="api_scatter"),
    path("api/radar/", views.api_radar, name="api_radar"),
]