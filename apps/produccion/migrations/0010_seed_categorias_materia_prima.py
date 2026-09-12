from django.db import migrations


CATEGORIAS = [
    ('Telas', 'Telas planas, de punto, ripstop, drill y uniformes.'),
    ('Hilos', 'Hilos de coser, bordar y remallar.'),
    ('Avíos', 'Botones, cremalleras, gomas, cintas y cierres.'),
    ('Forros y entretelas', 'Forros, entretelas y materiales de refuerzo.'),
    ('Etiquetas y empaques', 'Etiquetas, bolsas, cajas y material de empaque.'),
    ('Tintes y acabados', 'Tintes y productos autorizados para acabados textiles.'),
]


def seed_categories(apps, schema_editor):
    categoria = apps.get_model('produccion', 'CategoriaMateriaPrima')
    for nombre, descripcion in CATEGORIAS:
        categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion},
        )


def unseed_categories(apps, schema_editor):
    categoria = apps.get_model('produccion', 'CategoriaMateriaPrima')
    categoria.objects.filter(nombre__in=[nombre for nombre, _ in CATEGORIAS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('produccion', '0009_materiaprima_especificacion_tecnica_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
