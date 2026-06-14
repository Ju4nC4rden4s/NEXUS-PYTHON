from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Reservation(models.Model):
    class Status(models.TextChoices):
        RESERVED = "RESERVED", "Reserved"
        CANCELLED = "CANCELLED", "Cancelled"
        ATTENDED = "ATTENDED", "Attended"
        NO_SHOW = "NO_SHOW", "No Show"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    session = models.ForeignKey(
        "classes.ClassSession",
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RESERVED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "session"],
                name="unique_user_session"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.session}"

    def clean(self):
        # Validar que la sesión no esté cancelada
        if self.session_id:
            if self.session.status == "CANCELLED":
                raise ValidationError(
                    {"session": "No se puede reservar una sesión cancelada."}
                )

            # Validar que la sesión no haya pasado ya
            if self.session.start_datetime < timezone.now():
                raise ValidationError(
                    {"session": "No se puede reservar una sesión que ya ocurrió."}
                )

            # Validar que el usuario no sea el coach de la sesión
            if self.user_id and self.session.coach_id == self.user_id:
                raise ValidationError(
                    {"user": "El entrenador no puede reservar su propia sesión."}
                )

            # Validar que haya cupos disponibles
            if self.session.is_full:
                raise ValidationError(
                    {"session": f"La sesión está llena. Capacidad máxima: {self.session.capacity} personas."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)