from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0006_cuenta_contable_fields')]
    operations = [
        migrations.AddField(
            model_name='asientocontable',
            name='referencia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='asientocontable',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('general', 'Asiento general'),
                    ('compra', 'Compra'),
                    ('venta', 'Venta'),
                    ('nomina', 'Nómina'),
                    ('produccion', 'Producción'),
                    ('ajuste', 'Ajuste'),
                ],
                default='general',
                max_length=20,
            ),
        ),
    ]
