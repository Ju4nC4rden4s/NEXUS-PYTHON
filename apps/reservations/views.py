from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Reservation
from apps.classes.models import ClassSession


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def _friendly_reservation_error(error):
    messages = []
    if hasattr(error, 'message_dict'):
        for value in error.message_dict.values():
            if isinstance(value, (list, tuple)):
                messages.extend([str(item) for item in value])
            else:
                messages.append(str(value))
    else:
        messages = [str(error)]

    for msg in messages:
        if 'Reservation with this User and Session already exists' in msg or 'already exists' in msg:
            return 'Ya tienes una reserva activa para esta sesión.'
        if 'No se puede reservar una sesión cancelada' in msg:
            return msg
        if 'No se puede reservar una sesión que ya ocurrió' in msg:
            return msg
        if 'La sesión está llena' in msg:
            return msg
        if 'El entrenador no puede reservar su propia sesión' in msg:
            return msg
    return 'No se pudo crear la reserva. Intenta de nuevo.'


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
        friendly_message = 'No se pudo crear la reserva. Intenta de nuevo.'
        try:
            reserva_existente = Reservation.objects.filter(
                user=request.user,
                session_id=session_id,
                status='CANCELLED'
            ).first()

            if reserva_existente:
                reserva_existente.status = 'RESERVED'
                reserva_existente.save()
            else:
                Reservation.objects.create(
                    user=request.user,
                    session_id=session_id
                )
            friendly_message = 'Reserva creada exitosamente.'
            if _is_ajax(request):
                return JsonResponse({'success': True, 'message': friendly_message})
            messages.success(request, friendly_message)
        except ValidationError as e:
            friendly_message = _friendly_reservation_error(e)
            if _is_ajax(request):
                return JsonResponse({'success': False, 'message': friendly_message})
            messages.error(request, friendly_message)
        except IntegrityError as e:
            friendly_message = 'Ya tienes una reserva activa para esta sesión.'
            if _is_ajax(request):
                return JsonResponse({'success': False, 'message': friendly_message})
            messages.error(request, friendly_message)
        except Exception:
            if _is_ajax(request):
                return JsonResponse({'success': False, 'message': friendly_message})
            messages.error(request, friendly_message)
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