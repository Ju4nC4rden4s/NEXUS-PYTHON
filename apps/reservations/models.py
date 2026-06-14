from django.db import models
from django.conf import settings


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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "session"],
                name="unique_user_session"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.session}"