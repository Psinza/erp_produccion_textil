import os

# Establecer el módulo de configuración de Django predeterminado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    from celery import Celery

    app = Celery('config')

    # Usar una cadena aquí significa que el trabajador no tiene que serializar
    # el objeto de configuración a procesos hijos.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # Descubrir tareas automáticamente en todas las apps registradas
    app.autodiscover_tasks()

    # Configuración de Celery por defecto
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'America/Caracas'
except ImportError:
    app = None