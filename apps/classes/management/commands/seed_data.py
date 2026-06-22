from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import User
from apps.classes.models import Class, ClassSession
from apps.reservations.models import Reservation


class Command(BaseCommand):
    help = "Poblar la base de datos con datos de prueba."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando seed de datos..."))

        clients = self._create_clients()
        coaches = self._create_coaches()
        classes = self._create_classes()
        sessions = self._create_sessions(classes, coaches)
        self._create_reservations(clients, sessions)

        self.stdout.write(self.style.SUCCESS("Seed de datos completado correctamente."))

    def _create_clients(self):
        clients = []
        for i in range(1, 21):
            username = f"cliente{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "role": User.Roles.CLIENT,
                },
            )
            if created:
                user.set_password("1234")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Cliente creado: {username}"))
            clients.append(user)
        return clients

    def _create_coaches(self):
        coaches = []
        for i in range(1, 11):
            username = f"coach{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "role": User.Roles.COACH,
                },
            )
            if created:
                user.set_password("1234")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Coach creado: {username}"))
            else:
                # Asegurar rol COACH si existe previamente
                if user.role != User.Roles.COACH:
                    user.role = User.Roles.COACH
                    user.save()
            coaches.append(user)
        return coaches

    def _create_classes(self):
        class_definitions = [
            {"name": "Muay Thai", "duration_minutes": 60, "level": Class.Levels.INTERMEDIATE},
            {"name": "Jiu-Jitsu", "duration_minutes": 75, "level": Class.Levels.ADVANCED},
            {"name": "Boxeo", "duration_minutes": 45, "level": Class.Levels.BEGINNER},
            {"name": "MMA", "duration_minutes": 90, "level": Class.Levels.ADVANCED},
            {"name": "Kickboxing", "duration_minutes": 60, "level": Class.Levels.INTERMEDIATE},
            {"name": "Judo", "duration_minutes": 50, "level": Class.Levels.BEGINNER},
            {"name": "Karate", "duration_minutes": 55, "level": Class.Levels.BEGINNER},
            {"name": "Taekwondo", "duration_minutes": 65, "level": Class.Levels.INTERMEDIATE},
            {"name": "Krav Maga", "duration_minutes": 80, "level": Class.Levels.ADVANCED},
            {"name": "Lucha Libre", "duration_minutes": 70, "level": Class.Levels.INTERMEDIATE},
        ]

        classes = []
        for data in class_definitions:
            gym_class, created = Class.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": f"Clase de {data['name']} de nivel {data['level']}.",
                    "duration_minutes": data["duration_minutes"],
                    "level": data["level"],
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Clase creada: {gym_class.name}"))
            else:
                gym_class.description = f"Clase de {data['name']} de nivel {data['level']}."
                gym_class.duration_minutes = data["duration_minutes"]
                gym_class.level = data["level"]
                gym_class.is_active = True
                gym_class.save()
            classes.append(gym_class)
        return classes

    def _create_sessions(self, classes, coaches):
        sessions = []
        today = timezone.now()

        for gym_class in classes:
            session_date = today + timedelta(days=random.randint(1, 7))
            start_datetime = session_date.replace(
                hour=random.choice([8, 10, 12, 14, 16, 18, 20]),
                minute=0,
                second=0,
                microsecond=0,
            )
            coach = random.choice(coaches)
            capacity = random.randint(5, 8)

            session, created = ClassSession.objects.get_or_create(
                gym_class=gym_class,
                start_datetime=start_datetime,
                defaults={
                    "coach": coach,
                    "capacity": capacity,
                    "status": ClassSession.Status.SCHEDULED,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Sesión creada: {gym_class.name} con coach {coach.username} el {start_datetime}."
                ))
            else:
                session.coach = coach
                session.capacity = capacity
                session.status = ClassSession.Status.SCHEDULED
                session.save()
            sessions.append(session)

        return sessions

    def _create_reservations(self, clients, sessions):
        available_sessions = [s for s in sessions if s.start_datetime > timezone.now() and not s.is_full]
        if not available_sessions:
            self.stdout.write(self.style.WARNING("No hay sesiones futuras disponibles para reservar."))
            return

        reserved = 0
        attempts = 0
        while reserved < 5 and attempts < 30:
            attempts += 1
            session = random.choice(available_sessions)
            user = random.choice(clients)

            if session.is_full:
                continue

            already_reserved = Reservation.objects.filter(user=user, session=session).exists()
            if already_reserved:
                continue

            try:
                reservation = Reservation.objects.create(
                    user=user,
                    session=session,
                    status=Reservation.Status.RESERVED,
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Reserva creada: {user.username} en sesión {session}."
                ))
                reserved += 1
            except Exception as exc:
                self.stdout.write(self.style.WARNING(
                    f"No se pudo crear reserva para {user.username} en {session}: {exc}"
                ))
                continue

            if session.is_full:
                available_sessions = [s for s in available_sessions if not s.is_full]

        if reserved < 5:
            self.stdout.write(self.style.WARNING(
                f"Solo se crearon {reserved} reservas activas."
            ))
