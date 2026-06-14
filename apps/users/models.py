from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        COACH = "COACH", "Entrenador"
        CLIENT = "CLIENT", "Cliente"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CLIENT
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )