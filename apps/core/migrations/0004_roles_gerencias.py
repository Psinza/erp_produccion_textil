from django.db import migrations


AREAS = {
    'PRODUCCION': 'Producción',
    'LOGISTICA': 'Logística',
    'COMPRAS': 'Compras',
    'COMERCIALIZACION': 'Comercialización',
    'TRANSPORTE': 'Transportes',
    'FINANZAS': 'Finanzas',
    'TALENTO_HUMANO': 'Talento Humano',
    'ACTIVOS': 'Activos Fijos',
    'GERENCIA': 'Gerencia',
}

ROLES = {
    'Gerencia de Producción': 'PRODUCCION',
    'Gerencia de Logística': 'LOGISTICA',
    'Gerencia de Compras': 'COMPRAS',
    'Gerencia de Comercialización': 'COMERCIALIZACION',
    'Gerencia de Transportes': 'TRANSPORTE',
    'Gerencia de Finanzas': 'FINANZAS',
    'Gerencia de Talento Humano': 'TALENTO_HUMANO',
    'Gerencia de Activos Fijos': 'ACTIVOS',
    'Gerencia General': 'GERENCIA',
}


def create_access_roles(apps, schema_editor):
    Area = apps.get_model('core', 'Area')
    Rol = apps.get_model('core', 'Rol')
    for codigo, nombre in AREAS.items():
        area, _ = Area.objects.get_or_create(
            codigo=codigo,
            defaults={'nombre': nombre, 'activo': True},
        )
        for rol_nombre, rol_codigo in ROLES.items():
            if rol_codigo == codigo:
                rol, _ = Rol.objects.get_or_create(
                    nombre=rol_nombre,
                    defaults={
                        'descripcion': f'Acceso restringido al módulo de {nombre}.',
                        'nivel': 'LECTURA_ESCRITURA',
                        'activo': True,
                    },
                )
                rol.areas.add(area)


class Migration(migrations.Migration):
    dependencies = [('core', '0003_alter_tasabcv_eur_ves_alter_tasabcv_usd_ves')]
    operations = [migrations.RunPython(create_access_roles, migrations.RunPython.noop)]
