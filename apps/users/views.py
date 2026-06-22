from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from apps.classes.models import Class, ClassSession
from apps.reservations.models import Reservation
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

def home(request):
    return render(request, 'home.html', {
        'user': request.user,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == User.Roles.ADMIN:
                return redirect(f"{reverse('login')}?error=role_mismatch")
            auth_login(request, user)
            return redirect('dashboard')
        return redirect(f"{reverse('login')}?error=true")

    return render(request, 'registration/login.html', {
        'open_admin_modal': request.GET.get('admin') == '1'
    })


def admin_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {
            'open_admin_modal': True,
        })

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user.role != User.Roles.ADMIN:
            return redirect(f"{reverse('login')}?error=role_mismatch&admin=1")
        auth_login(request, user)
        return redirect('dashboard')

    return redirect(f"{reverse('login')}?error=true&admin=1")


def register(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip().lower()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password', '')

        User.objects.create_user(
            username=nombre.lower() + apellido.lower(),
            email=correo,
            first_name=nombre,
            last_name=apellido,
            phone=telefono,
            password=password,
            role=User.Roles.CLIENT
        )

        messages.success(
            request,
            'Cuenta creada correctamente. Ya puedes iniciar sesión.'
        )

        return redirect('login')

    return render(request, 'registro.html')

def register_admin(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip().lower()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password', '')

        User.objects.create_user(
            username=nombre.lower() + apellido.lower(),
            email=correo,
            first_name=nombre,
            last_name=apellido,
            phone=telefono,
            password=password,
            role=User.Roles.ADMIN
        )

        messages.success(
            request,
            'Cuenta de administrador creada correctamente. Ya puedes iniciar sesión.'
        )

        return redirect('admin_login')

    return render(request, 'registration/registroAdmin.html')

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