from . import views
from django.urls import path

urlpatterns = [
    path("get/all/<int:index>/", views.getProducts),
    path("get/by-ids/", views.getProductsByIds),
    path("get/<int:id>/", views.getProductDetails),
    path("similar/<int:id>/", views.getSimilarProducts),
]