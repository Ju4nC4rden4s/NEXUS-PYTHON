# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Coach


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('role', 'phone')}),
    )


@admin.register(Coach)
class CoachAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('phone',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('phone',)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role=User.Roles.COACH)

    def save_model(self, request, obj, form, change):
        obj.role = User.Roles.COACH
        super().save_model(request, obj, form, change)