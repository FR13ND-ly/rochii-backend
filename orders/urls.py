from . import views
from django.urls import path

urlpatterns = [
    path("create/", views.createOrder),
    path("get-available-hours/", views.getAvailableHours),
]