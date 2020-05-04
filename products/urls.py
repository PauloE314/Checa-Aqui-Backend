from django.urls import path
from products import views

urlpatterns = [
    path('', views.Products.as_view()),
    path('detail/', views.DetailProducts.as_view()),
    path('types/', views.ProductTypes.as_view()),
    path('stores/', views.Stores.as_view())
]
