from . import views
from django.urls import path

urlpatterns = [
    path("upload-image/", views.uploadImage),
    path("serve-image/<int:imageId>/", views.serveImage),
]