from django.db import migrations


ALMACENES = [
    ('Almacén de Repuestos de Máquinas', 'repuestos', 'Mantenimiento de confección'),
    ('Almacén de Telas e Hilos', 'materias_primas', 'Materia prima textil'),
    ('Almacén de Consumibles Textiles', 'consumibles', 'Botones, cremalleras, gomas y cintas'),
    ('Almacén de Producto Terminado', 'producto_terminado', 'Prendas liberadas por Pool'),
]


def seed_almacenes(apps, schema_editor):
    almacen = apps.get_model('logistica', 'Almacen')
    for nombre, tipo, ubicacion in ALMACENES:
        almacen.objects.get_or_create(
            nombre=nombre,
            defaults={'tipo': tipo, 'ubicacion': ubicacion, 'activo': True},
        )


def unseed_almacenes(apps, schema_editor):
    almacen = apps.get_model('logistica', 'Almacen')
    almacen.objects.filter(nombre__in=[item[0] for item in ALMACENES]).delete()


class Migration(migrations.Migration):
    dependencies = [('logistica', '0003_repuestomaquina_and_more')]
    operations = [migrations.RunPython(seed_almacenes, unseed_almacenes)]
