import json

from django.db.models import Q, Count, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Class, ClassSession
from apps.reservations.models import Reservation
from apps.users.models import User


@login_required
def classes_list(request):
    clases = Class.objects.all().order_by('name')

    name_filter = request.GET.get('name', '').strip()
    level_filter = request.GET.get('level', '')
    status_filter = request.GET.get('status', '')
    min_duration = request.GET.get('min_duration', '').strip()
    max_duration = request.GET.get('max_duration', '').strip()

    if name_filter:
        clases = clases.filter(name__icontains=name_filter)

    if level_filter in [Class.Levels.BEGINNER, Class.Levels.INTERMEDIATE, Class.Levels.ADVANCED]:
        clases = clases.filter(level=level_filter)

    if status_filter == 'active':
        clases = clases.filter(is_active=True)
    elif status_filter == 'inactive':
        clases = clases.filter(is_active=False)

    if min_duration.isdigit():
        clases = clases.filter(duration_minutes__gte=int(min_duration))

    if max_duration.isdigit():
        clases = clases.filter(duration_minutes__lte=int(max_duration))

    now = timezone.now()
    upcoming_sessions = ClassSession.objects.filter(
        status=ClassSession.Status.SCHEDULED,
        start_datetime__gt=now
    ).order_by('start_datetime')

    available_sessions_by_class = {}
    for session in upcoming_sessions:
        if session.is_full:
            continue

        available_sessions_by_class.setdefault(session.gym_class_id, []).append({
            'id': session.pk,
            'datetime': session.start_datetime.strftime('%d/%m/%Y %H:%M'),
            'coach': session.coach.get_full_name() or session.coach.username,
            'available_spots': session.available_spots,
        })

    sessions_json = json.dumps(available_sessions_by_class)

    return render(request, 'classes.html', {
        'clases': clases,
        'user': request.user,
        'available_class_ids': list(available_sessions_by_class.keys()),
        'available_sessions_by_class': available_sessions_by_class,
        'available_sessions_json': sessions_json,
        'available_sessions_by_class_json': sessions_json,
        'filters': {
            'name': name_filter,
            'level': level_filter,
            'status': status_filter,
            'min_duration': min_duration,
            'max_duration': max_duration,
        },
        'results_count': clases.count(),
    })

@login_required
def class_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        duration_minutes = request.POST.get('duration_minutes')
        level = request.POST.get('level')

        Class.objects.create(
            name=name,
            description=description,
            duration_minutes=duration_minutes,
            level=level
        )
        return redirect('classes')

    return render(request, 'classes.html', {
        'clases': Class.objects.all(),
        'show_form': True,
        'user': request.user
    })


@login_required
def class_toggle(request, pk):
    clase = get_object_or_404(Class, pk=pk)
    clase.is_active = not clase.is_active
    clase.save()
    return redirect('classes')


@login_required
def sessions_list(request):
    if request.user.role not in (User.Roles.ADMIN, User.Roles.COACH):
        return redirect('dashboard')

    sesiones = ClassSession.objects.all().order_by('start_datetime')
    clases = Class.objects.filter(is_active=True)
    coaches = User.objects.filter(role=User.Roles.COACH)

    class_filter = request.GET.get('class_id', '')
    coach_filter = request.GET.get('coach', '')
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    has_spots = request.GET.get('has_spots') == '1'

    if class_filter.isdigit():
        sesiones = sesiones.filter(gym_class_id=int(class_filter))

    if coach_filter.isdigit():
        sesiones = sesiones.filter(coach_id=int(coach_filter))

    if status_filter in [ClassSession.Status.SCHEDULED, ClassSession.Status.CANCELLED, ClassSession.Status.COMPLETED]:
        sesiones = sesiones.filter(status=status_filter)

    if date_from:
        sesiones = sesiones.filter(start_datetime__date__gte=date_from)

    if date_to:
        sesiones = sesiones.filter(start_datetime__date__lte=date_to)

    sesiones = sesiones.annotate(
        reserved_count=Count('reservations', filter=~Q(
            reservations__status=Reservation.Status.CANCELLED))
    )

    if has_spots:
        sesiones = sesiones.filter(capacity__gt=F('reserved_count'))

    return render(request, 'sessions.html', {
        'sesiones': sesiones,
        'clases': clases,
        'coaches': coaches,
        'user': request.user,
        'filters': {
            'class_id': class_filter,
            'coach': coach_filter,
            'status': status_filter,
            'date_from': date_from,
            'date_to': date_to,
            'has_spots': has_spots,
        },
        'results_count': sesiones.count(),
        'show_form': request.GET.get('new') == '1' and request.user.role == User.Roles.ADMIN,
    })


@login_required
def session_create(request):
    if request.user.role != User.Roles.ADMIN:
        return redirect('dashboard')

    if request.method == 'POST':
        gym_class_id = request.POST.get('gym_class')
        coach_id = request.POST.get('coach')
        start_datetime = request.POST.get('start_datetime')
        capacity = request.POST.get('capacity')

        ClassSession.objects.create(
            gym_class_id=gym_class_id,
            coach_id=coach_id,
            start_datetime=start_datetime,
            capacity=capacity
        )
        return redirect('sessions')

    clases = Class.objects.filter(is_active=True)
    coaches = User.objects.filter(role='COACH')
    return render(request, 'sessions.html', {
        'sesiones': ClassSession.objects.all().order_by('start_datetime'),
        'clases': clases,
        'coaches': coaches,
        'show_form': True,
        'user': request.user
    })


@login_required
def class_edit(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('classes')

    clase = get_object_or_404(Class, pk=pk)

    if request.method == 'POST':
        clase.name = request.POST.get('name')
        clase.description = request.POST.get('description')
        clase.duration_minutes = request.POST.get('duration_minutes')
        clase.level = request.POST.get('level')
        clase.save()
        return redirect('classes')

    return render(request, 'class_edit.html', {
        'clase': clase,
        'user': request.user
    })


@login_required
def class_delete(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('classes')

    clase = get_object_or_404(Class, pk=pk)
    clase.delete()
    return redirect('classes')
