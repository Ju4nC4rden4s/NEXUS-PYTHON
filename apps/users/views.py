from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.classes.models import Class, ClassSession
from apps.reservations.models import Reservation
from apps.users.models import User


@login_required
def dashboard(request):
    hoy = timezone.now().date()

    clases_activas = Class.objects.filter(is_active=True).count()
    sesiones_hoy = ClassSession.objects.filter(
        start_datetime__date=hoy,
        status='SCHEDULED'
    ).count()
    reservas_totales = Reservation.objects.count()
    usuarios_registrados = User.objects.count()

    return render(request, 'dashboard.html', {
        'user': request.user,
        'clases_activas': clases_activas,
        'sesiones_hoy': sesiones_hoy,
        'reservas_totales': reservas_totales,
        'usuarios_registrados': usuarios_registrados,
    })