from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.users_list, name='users'),
    path('usuarios/<int:pk>/toggle/', views.user_toggle, name='user_toggle'),
]