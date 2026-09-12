import os
from pathlib import Path

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (usa variable de entorno o fallback para desarrollo)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-erp-produccion-textil-sustituir-en-produccion')
)

# Modo depuración
DEBUG = os.environ.get('DJANGO_DEBUG', os.environ.get('DEBUG', 'True')).strip().lower() in ('true', '1', 't', 'yes')

# Hosts permitidos
_env_hosts = os.environ.get('ALLOWED_HOSTS', os.environ.get('DJANGO_ALLOWED_HOSTS', ''))
if _env_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _env_hosts.replace(' ', ',').split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.onrender.com', '.cloudshell.dev', '*']

# Orígenes confiables CSRF
_env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if _env_csrf:
    CSRF_TRUSTED_ORIGINS = [c.strip() for c in _env_csrf.replace(' ', ',').split(',') if c.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.onrender.com',
        'https://*.cloudshell.dev',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Núcleo del Sistema (Debe ir primero para AUTH_USER_MODEL)
    'apps.core.apps.CoreConfig', 
    
    # Módulos Funcionales
    'apps.contabilidad',
    'apps.vendedores',
    'apps.compras',
    'apps.ventas',
    'apps.activos_fijos',
    'apps.ordenacion_pagos',
    'apps.comercializacion',
    'apps.produccion',
    'apps.logistica',
    'apps.facturacion',
    'apps.viaticos',
    'apps.transportes',
    'apps.tesoreria',
    'apps.inventarios.apps.InventariosConfig',
    'apps.administracion',
    'apps.rrhh',
    'apps.gerencia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Soporte de archivos estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.access.GerenciaAccessMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.administracion.context_processors.empresa_context',
                'apps.core.context_processors.module_access',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ── Base de datos híbrida (Supabase PostgreSQL / SQLite local) ───────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ve'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# Modelo de Usuario Personalizado
AUTH_USER_MODEL = 'core.Usuario'

# Archivos estáticos (WhiteNoise para producción)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ERP_CONFIG = {
    'EMPRESA_NOMBRE': os.environ.get('EMPRESA_NOMBRE', 'Fábrica de Limpieza S.A.'),
    'VERSION': '1.0.0'
}

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Configuración de Celery resiliente (opcional)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

try:
    from celery.schedules import crontab
    CELERY_BEAT_SCHEDULE = {
        'enviar-reporte-mensual-fin-mes': {
            'task': 'apps.contabilidad.tasks.enviar_reporte_mensual_task',
            'schedule': crontab(minute=55, hour=23, day_of_month='28-31'),
            'description': 'Ejecuta el envío del reporte financiero el último día de cada mes a las 23:55'
        },
    }
except ImportError:
    CELERY_BEAT_SCHEDULE = {}

# Configuración de Correo SMTP
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tu-correo@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tu-contrasena-de-aplicacion')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', f"Sistema ERP <{EMAIL_HOST_USER}>")
SERVER_EMAIL = EMAIL_HOST_USER
