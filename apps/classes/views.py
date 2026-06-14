from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Class, ClassSession
from apps.users.models import User


@login_required
def classes_list(request):
    clases = Class.objects.all().order_by('name')
    return render(request, 'classes.html', {
        'clases': clases,
        'user': request.user
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
    sesiones = ClassSession.objects.all().order_by('start_datetime')
    return render(request, 'sessions.html', {
        'sesiones': sesiones,
        'user': request.user
    })


@login_required
def session_create(request):
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