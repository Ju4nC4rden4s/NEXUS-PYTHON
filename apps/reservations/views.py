from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation
from apps.classes.models import ClassSession


@login_required
def reservations_list(request):
    if request.user.role == 'ADMIN':
        reservas = Reservation.objects.all().order_by('-created_at')
    else:
        reservas = Reservation.objects.filter(
            user=request.user
        ).order_by('-created_at')

    return render(request, 'reservations.html', {
        'reservas': reservas,
        'user': request.user
    })


@login_required
def reservation_create(request):
    if request.method == 'POST':
        session_id = request.POST.get('session')
        try:
            Reservation.objects.create(
                user=request.user,
                session_id=session_id
            )
            messages.success(request, 'Reserva creada exitosamente.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('reservations')

    sesiones = ClassSession.objects.filter(
        status='SCHEDULED'
    ).order_by('start_datetime')

    return render(request, 'reservations.html', {
        'reservas': Reservation.objects.filter(user=request.user),
        'sesiones': sesiones,
        'show_form': True,
        'user': request.user
    })


@login_required
def reservation_cancel(request, pk):
    reserva = get_object_or_404(Reservation, pk=pk, user=request.user)
    reserva.status = 'CANCELLED'
    reserva.save()
    return redirect('reservations')