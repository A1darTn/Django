from django.urls import path
from .views import (
    SensorListCreateView,
    MeasurementCreatetView,
    SensorRetrieveUpdateView,
    SensorDetailView,
)


urlpatterns = [
    path("sensors/", SensorListCreateView.as_view()),
    path("sensors/<int:pk>/", SensorRetrieveUpdateView.as_view()),
    path("measurements/", MeasurementCreatetView.as_view()),
    path("sensors/<int:pk>/detail/", SensorDetailView.as_view()),
]
