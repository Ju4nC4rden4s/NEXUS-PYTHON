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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.gym_class.name} - "
            f"{self.start_datetime}"
        )
    
    