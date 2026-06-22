from django.db.models import Q
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
    
    username_filter = request.GET.get('username', '').strip()
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')

    usuarios = User.objects.all().order_by('role', 'username')

    if username_filter:
        usuarios = usuarios.filter(
            Q(username__icontains=username_filter) |
            Q(first_name__icontains=username_filter) |
            Q(last_name__icontains=username_filter)
        )

    if role_filter in [User.Roles.ADMIN, User.Roles.COACH, User.Roles.CLIENT]:
        usuarios = usuarios.filter(role=role_filter)

    if status_filter == 'active':
        usuarios = usuarios.filter(is_active=True)
    elif status_filter == 'inactive':
        usuarios = usuarios.filter(is_active=False)

    return render(request, 'users.html', {
        'usuarios': usuarios,
        'user': request.user,
        'filters': {
            'username': username_filter,
            'role': role_filter,
            'status': status_filter,
        },
        'results_count': usuarios.count(),
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

    name_filter = request.GET.get('name', '').strip()
    status_filter = request.GET.get('status', '')

    coaches = User.objects.filter(
        role=User.Roles.COACH
    ).order_by('username')

    if name_filter:
        coaches = coaches.filter(
            Q(username__icontains=name_filter) |
            Q(first_name__icontains=name_filter) |
            Q(last_name__icontains=name_filter)
        )

    if status_filter == 'active':
        coaches = coaches.filter(is_active=True)
    elif status_filter == 'inactive':
        coaches = coaches.filter(is_active=False)

    return render(
        request,
        'coaches.html',
        {
            'coaches': coaches,
            'filters': {
                'name': name_filter,
                'status': status_filter,
            },
            'results_count': coaches.count(),
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