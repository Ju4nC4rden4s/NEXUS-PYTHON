from django.urls import path
from . import views

urlpatterns = [
    path('clases/', views.classes_list, name='classes'),
    path('clases/crear/', views.class_create, name='class_create'),
    path('clases/<int:pk>/toggle/', views.class_toggle, name='class_toggle'),
    path('clases/<int:pk>/editar/', views.class_edit, name='class_edit'),
    path('clases/<int:pk>/eliminar/', views.class_delete, name='class_delete'),
    path('sesiones/', views.sessions_list, name='sessions'),
    path('sesiones/crear/', views.session_create, name='session_create'),
]