from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/administrator/', include('administrator.urls')),
    path('api/files/', include('files.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/products/', include('products.urls')),
    path('admin/', admin.site.urls),
]
