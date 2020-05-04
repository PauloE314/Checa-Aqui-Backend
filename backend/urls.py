from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('products/', include('products.urls')),
    path('attendance/', include('attendance.urls'))
]
