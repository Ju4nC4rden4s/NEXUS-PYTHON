from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.classes.models import Class, ClassSession
from apps.reservations.models import Reservation
from apps.users.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.users.models import User, Coach


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

@login_required
def coaches_list(request):

    if request.user.role != User.Roles.ADMIN:
        return redirect('dashboard')

    coaches = User.objects.filter(
        role=User.Roles.COACH
    ).order_by('username')

    return render(
        request,
        'coaches.html',
        {
            'coaches': coaches
        }
    )

@login_required
def coach_create(request):

    if request.user.role != User.Roles.ADMIN:
        return redirect('dashboard')

    if request.method == 'POST':

        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            phone=request.POST.get('phone', ''),
            password=request.POST['password'],
            role=User.Roles.COACH
        )

        messages.success(
            request,
            'Entrenador creado correctamente.'
        )

        return redirect('coaches')

    coaches = User.objects.filter(
        role=User.Roles.COACH
    )

    return render(
        request,
        'coaches.html',
        {
            'coaches': coaches,
            'show_form': True
        }
    )


@login_required
def coach_toggle(request, pk):

    if request.user.role != User.Roles.ADMIN:
        return redirect('dashboard')

    coach = get_object_or_404(
        User,
        pk=pk,
        role=User.Roles.COACH
    )

    coach.is_active = not coach.is_active
    coach.save()

    return redirect('coaches')