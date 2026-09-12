from django.db import migrations


def create_sales_role(apps, schema_editor):
    Area = apps.get_model('core', 'Area')
    Rol = apps.get_model('core', 'Rol')
    area, _ = Area.objects.get_or_create(
        codigo='VENTAS',
        defaults={'nombre': 'Ventas', 'activo': True},
    )
    rol, _ = Rol.objects.get_or_create(
        nombre='Gerencia de Ventas',
        defaults={
            'descripcion': 'Acceso restringido al módulo de Ventas.',
            'nivel': 'LECTURA_ESCRITURA',
            'activo': True,
        },
    )
    rol.areas.add(area)


class Migration(migrations.Migration):
    dependencies = [('core', '0004_roles_gerencias')]
    operations = [migrations.RunPython(create_sales_role, migrations.RunPython.noop)]
