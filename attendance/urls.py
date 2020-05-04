from django.urls import path
from attendance import views

urlpatterns = [
    path('client/', views.ClientAttendances.as_view()), #ATENDIMENTOS EM QUE O USER É O ATENDIDO
    path('attendant/', views.AttendantAttendances.as_view()), #ATENDIMENTOS EM QUE O USER É O ATENDENTE
    path('<int:pk>/', views.DetailAttendances.as_view()),


    path('<int:pk>/client-avaliate/', views.Client_Evaluate_Attendant.as_view()),
    path('<int:pk>/attendant-avaliate/', views.Attendant_Evaluate_Client.as_view()),
]
