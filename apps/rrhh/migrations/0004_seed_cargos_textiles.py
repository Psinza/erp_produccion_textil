from django.db import migrations


CARGOS = [
    ('Producción', 'Supervisor de Producción'),
    ('Producción', 'Operario de Corte'),
    ('Producción', 'Operario de Confección'),
    ('Producción', 'Inspector de Calidad Textil'),
    ('Tecnologia', 'Analista de Sistemas'),
    ('Comercialización', 'Ejecutivo de Ventas'),
    ('Seguridad', 'Oficial de Seguridad'),
    ('Transporte', 'Conductor'),
    ('Logistica', 'Analista de Inventario'),
    ('Administracción', 'Asistente Administrativo'),
    ('Comunicaciones', 'Analista de Comunicaciones'),
    ('Consultoria Juridica', 'Analista Jurídico'),
    ('Contrataciones Publica', 'Analista de Contrataciones'),
    ('Talento Humano', 'Analista de Talento Humano'),
]


def seed_cargos(apps, schema_editor):
    departamento = apps.get_model('rrhh', 'Departamento')
    cargo = apps.get_model('rrhh', 'Cargo')
    for departamento_nombre, cargo_nombre in CARGOS:
        dep = departamento.objects.filter(nombre=departamento_nombre).first()
        if dep:
            cargo.objects.get_or_create(
                nombre=cargo_nombre,
                departamento=dep,
                defaults={'nivel': 'operativo', 'sector': 'privado'},
            )


def unseed_cargos(apps, schema_editor):
    cargo = apps.get_model('rrhh', 'Cargo')
    cargo.objects.filter(nombre__in=[nombre for _, nombre in CARGOS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('rrhh', '0003_empleado_banco_pago_empleado_tipo_cuenta_pago_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_cargos, unseed_cargos),
    ]
