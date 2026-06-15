from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.classes.models import Class, ClassSession
from apps.reservations.models import Reservation
from apps.users.models import User
from django.shortcuts import render, redirect, get_object_or_404


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

@login_required
def users_list(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    usuarios = User.objects.all().order_by('role', 'username')
    return render(request, 'users.html', {
        'usuarios': usuarios,
        'user': request.user
    })


@login_required
def user_toggle(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect('users')