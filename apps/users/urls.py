from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.users_list, name='users'),
    path('usuarios/<int:pk>/toggle/', views.user_toggle, name='user_toggle'),
    path('coaches/', views.coaches_list, name='coaches'),
    path('coaches/crear/', views.coach_create, name='coach_create'),
    path('coaches/<int:pk>/toggle/', views.coach_toggle, name='coach_toggle'),
]