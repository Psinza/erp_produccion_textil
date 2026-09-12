from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0005_gerencia_ventas')]
    operations = [
        migrations.AddField(
            model_name='cuentacontable',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='cuentacontable',
            name='nivel',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cuentacontable',
            name='naturaleza',
            field=models.CharField(
                choices=[
                    ('deudora', 'Deudora'),
                    ('acreedora', 'Acreedora'),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='cuentacontable',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('activo', 'Activo'),
                    ('pasivo', 'Pasivo'),
                    ('patrimonio', 'Patrimonio / Capital'),
                    ('ingreso', 'Ingreso'),
                    ('gasto', 'Gasto / Egreso'),
                ],
                max_length=20,
            ),
        ),
    ]
