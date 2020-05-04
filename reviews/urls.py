from django.urls import path

from reviews import views

urlpatterns = [
    path('', views.Reviews.as_view()),
    path('<int:pk>/', views.DetailReview.as_view()),
    path('self/', views.SelfReviews.as_view()),
    path('<int:pk>/like/', views.LikeReview.as_view())
]