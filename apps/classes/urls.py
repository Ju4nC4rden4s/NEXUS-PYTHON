from django.urls import path
from . import views

urlpatterns = [
    path('clases/', views.classes_list, name='classes'),
    path('clases/crear/', views.class_create, name='class_create'),
    path('clases/<int:pk>/toggle/', views.class_toggle, name='class_toggle'),
    path('sesiones/', views.sessions_list, name='sessions'),
    path('sesiones/crear/', views.session_create, name='session_create'),
]