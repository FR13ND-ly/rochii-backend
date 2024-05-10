from . import views
from django.urls import path

urlpatterns = [
    path("authentification/", views.authentificate),
    path("authorization/<str:token>/", views.authorization),

    path("products/get/all/<int:index>/", views.getProducts),
    path("products/get/<int:id>/", views.getProductById),
    path("products/create/", views.createProduct),
    path("products/update/<int:id>/", views.updateProduct),
    path("products/delete/<int:id>/", views.deleteProduct),

    path("orders/get/<int:index>/", views.getOrders),
    path("orders/complete/<int:id>/", views.completeOrder),
    path("orders/delete/<int:id>/", views.deleteOrder),

    path("dashboard/", views.getDashboard),
    path("statistics/", views.getStatistics),
]