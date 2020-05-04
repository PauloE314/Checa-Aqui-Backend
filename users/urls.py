from django.urls import path
from rest_framework.authtoken import views as v

from users import views


urlpatterns = [
    path('token-login/', v.obtain_auth_token),
    path('authenticate-email/', views.ActiveAccount.as_view()),

    path('', views.Users.as_view()),
    path('self/', views.DetailSelf.as_view()),
    path('<int:pk>/', views.DetailUsers.as_view())
]
