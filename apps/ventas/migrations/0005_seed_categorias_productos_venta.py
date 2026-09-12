from django.db import migrations


CATEGORIAS = [
    'Uniformes militares',
    'Ropa institucional',
    'Uniformes deportivos',
    'Ropa escolar',
    'Telas y tejidos',
    'Accesorios y avíos',
]


def seed_categories(apps, schema_editor):
    categoria = apps.get_model('ventas', 'CategoriaProductoVenta')
    for nombre in CATEGORIAS:
        categoria.objects.get_or_create(nombre=nombre)


def unseed_categories(apps, schema_editor):
    categoria = apps.get_model('ventas', 'CategoriaProductoVenta')
    categoria.objects.filter(nombre__in=CATEGORIAS).delete()


class Migration(migrations.Migration):
    dependencies = [('ventas', '0004_detallepedido_orden_produccion_productoventa_colores_and_more')]
    operations = [migrations.RunPython(seed_categories, unseed_categories)]
