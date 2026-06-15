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

### 6. Correr el servidor
```bash
python manage.py runserver
```

### 7. Acceder al sistema
Abre el navegador en `http://127.0.0.1:8000/`

## Módulos

- **Usuarios** — gestión de usuarios con roles (Admin, Entrenador, Cliente)
- **Clases** — gestión de clases con niveles y estado
- **Sesiones** — programación de sesiones con coach y capacidad máxima de 8 personas
- **Reservas** — reserva de cupos en sesiones con validaciones de negocio