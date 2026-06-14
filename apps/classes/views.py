from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Class


@login_required
def classes_list(request):
    clases = Class.objects.all().order_by('name')
    return render(request, 'classes.html', {
        'clases': clases
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
        'show_form': True
    })


@login_required
def class_toggle(request, pk):
    clase = get_object_or_404(Class, pk=pk)
    clase.is_active = not clase.is_active
    clase.save()
    return redirect('classes')

@login_required
def classes_list(request):
    print(f"Usuario: {request.user.username} - Rol: {request.user.role}")
    clases = Class.objects.all().order_by('name')
    return render(request, 'classes.html', {
        'clases': clases
    })