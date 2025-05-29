from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('exercise/', views.exercise, name='exercise'), 
    path('complete-workout/', views.complete_workout, name='complete_workout'), 
    path('schedule-email/', views.schedule_email, name='schedule_email'),
    
]
