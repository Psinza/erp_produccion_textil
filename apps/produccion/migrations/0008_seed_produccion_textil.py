from django.db import migrations


PROCESOS = [
    ('udp', 'UDP / Diseño', 'Definir diseño, ficha técnica y requerimiento de materiales.', '8.3', 'COVENIN 3133-1'),
    ('corte', 'Corte', 'Validar tela, tender y habilitar piezas conformes.', '8.5.1', 'COVENIN 2280'),
    ('produccion_textil', 'Producción textil', 'Confeccionar la prenda según ruta y línea asignada.', '8.5.1', 'COVENIN 2277'),
    ('pool', 'Pool de calidad', 'Verificar conformidad del producto antes de liberarlo.', '8.6', 'COVENIN  ISO 9001'),
    ('bordados', 'Bordados', 'Aplicar logos, nombres y emblemas conforme a la muestra aprobada.', '8.5.1', 'COVENIN 2277'),
    ('despacho', 'Despacho', 'Planchar, revisar fibras, empaquetar y entregar.', '8.5.4', 'COVENIN 2277'),
]

INDICADORES = [
    ('MERMA-TELA', 'Merma de tela', 'corte', 5, '%', 'menor', '8.5.1'),
    ('RECH-CORTE', 'Rechazo en corte', 'corte', 3, '%', 'menor', '8.6'),
    ('FPY-CONF', 'First Pass Yield de confección', 'produccion_textil', 95, '%', 'mayor', '9.1'),
    ('FPY-POOL', 'First Pass Yield del Pool', 'pool', 98, '%', 'mayor', '9.1'),
    ('RECH-BORD', 'Rechazo de bordados', 'bordados', 2, '%', 'menor', '8.6'),
    ('OTIF-DESP', 'Entrega completa y a tiempo', 'despacho', 95, '%', 'mayor', '9.1'),
]


def seed_catalogo(apps, schema_editor):
    catalogo = apps.get_model('produccion', 'CatalogoProceso')
    indicador = apps.get_model('produccion', 'IndicadorProceso')
    for codigo, nombre, objetivo, clausula, norma in PROCESOS:
        catalogo.objects.update_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'objetivo': objetivo,
                'clausula_iso': clausula,
                'norma_venezolana': norma,
                'activo': True,
            },
        )
    for codigo, nombre, departamento, objetivo, unidad, sentido, clausula in INDICADORES:
        indicador.objects.update_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'departamento': departamento,
                'objetivo': objetivo,
                'unidad': unidad,
                'tipo': 'porcentaje',
                'sentido': sentido,
                'clausula_iso': clausula,
                'activo': True,
            },
        )


def unseed_catalogo(apps, schema_editor):
    apps.get_model('produccion', 'IndicadorProceso').objects.filter(
        codigo__in=[item[0] for item in INDICADORES]
    ).delete()
    apps.get_model('produccion', 'CatalogoProceso').objects.filter(
        codigo__in=[item[0] for item in PROCESOS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [('produccion', '0007_catalogoproceso')]
    operations = [migrations.RunPython(seed_catalogo, unseed_catalogo)]
