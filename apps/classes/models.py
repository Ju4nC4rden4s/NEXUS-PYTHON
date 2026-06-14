from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Class(models.Model):
    class Levels(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    level = models.CharField(
        max_length=20,
        choices=Levels.choices,
        default=Levels.BEGINNER
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ClassSession(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    gym_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coaching_sessions"
    )
    start_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gym_class.name} - {self.start_datetime}"

    @property
    def reserved_spots(self):
        """Cuántas reservas activas tiene esta sesión."""
        return self.reservations.exclude(status="CANCELLED").count()

    @property
    def available_spots(self):
        """Cupos disponibles restantes."""
        return self.capacity - self.reserved_spots

    @property
    def is_full(self):
        """True si no hay cupos disponibles."""
        return self.available_spots <= 0

    def clean(self):
        # Validar que el coach tenga rol COACH
        if self.coach_id:
            if self.coach.role != "COACH":
                raise ValidationError(
                    {"coach": "El usuario asignado debe tener rol de Entrenador."}
                )

        # Validar que la capacidad sea mayor a 0 y máximo 8
        if self.capacity is not None:
            if self.capacity == 0:
                raise ValidationError(
                    {"capacity": "La capacidad debe ser mayor a 0."}
                )
            if self.capacity > 8:
                raise ValidationError(
                    {"capacity": "La capacidad máxima por sesión es de 8 personas."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)