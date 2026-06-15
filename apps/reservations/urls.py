from django.urls import path
from . import views

urlpatterns = [
    path('reservas/', views.reservations_list, name='reservations'),
    path('reservas/crear/', views.reservation_create, name='reservation_create'),
    path('reservas/<int:pk>/cancelar/', views.reservation_cancel, name='reservation_cancel'),
]