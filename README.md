# NEXUS-PYTHON

Módulo de gestión de clases y reservas para el gimnasio NEXUS MMA, desarrollado en Django.

## Requisitos

- Python 3.10+
- pip

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Ju4nC4rden4s/NEXUS-PYTHON.git
cd NEXUS-PYTHON
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Asignar rol ADMIN al superusuario
```bash
python manage.py shell
```
Dentro de la shell:
```python
from apps.users.models import User
u = User.objects.get(username='admin123')
u.role = 'ADMIN'
u.save()
exit()
```

### 7. Crear usuario cliente desde la shell
```bash
python manage.py shell
```
Dentro de la shell:
```python
from apps.users.models import User
User.objects.create_user(
    username='cliente1',
    password='1234',
    role='CLIENT',
    email='cliente@test.com'
)
exit()
```

### 8. Correr el servidor
```bash
python manage.py runserver
```

### 9. Acceder al sistema
Abre el navegador en `http://127.0.0.1:8000/`

## Roles del sistema

- **ADMIN** — gestión completa del sistema
- **COACH** — entrenador asignado a sesiones
- **CLIENT** — puede ver y reservar sesiones

## Módulos

- **Usuarios** — gestión de usuarios con roles
- **Clases** — gestión de clases con niveles y estado
- **Sesiones** — programación de sesiones con coach y capacidad máxima de 8 personas
- **Reservas** — reserva de cupos en sesiones con validaciones de negocio

## CREAR BD

1. ESTRUCTURA DE DATABASES EN CONFIG/SETTINGS.PY

# config/settings.py

import os  # Asegúrate de que este import esté al inicio del archivo

# ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_bd',        # Ejemplo: 'nexus_db'
        'USER': 'tu_usuario_postgres',     # Ejemplo: 'postgres'
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',               # O la IP de tu servidor
        'PORT': '5432',                    # Puerto por defecto de PostgreSQL
    }
}

2. SI NO SE SABEN LOS DATOS EJECUTAR ESTO EN TERMINAL

1 - sudo -i -u postgres
2 - psql
3 - \conninfo
4 - ALTER USER postgres WITH PASSWORD 'nueva_contraseña'; (si no recuerdan la contraseña)

## Con el entorno virtual activado ejecutar

1 - pip install psycopg2-binary
2 - python manage.py makemigrations
3 - python manage.py migrate

## CREAR SUPERUSUARIO

python manage.py createsuperuser

## ASIGNAR ROL ADMIN

python manage.py shell

Dentro de la shell:
  python
from apps.users.models import User
u = User.objects.get(username='admin123')
u.role = 'ADMIN'
u.save()
exit()

## EXCEL

Instalar dependencia

pip install openpyxl

