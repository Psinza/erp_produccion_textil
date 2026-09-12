from django.db import migrations, models


def set_ano_from_inicio(apps, schema_editor):
    EjercicioContable = apps.get_model('core', 'EjercicioContable')
    for ejercicio in EjercicioContable.objects.all():
        ejercicio.ano = ejercicio.fecha_inicio.year
        ejercicio.save(update_fields=['ano'])


class Migration(migrations.Migration):
    dependencies = [('core', '0007_asientocontable_tipo_referencia')]

    operations = [
        migrations.AddField(
            model_name='ejerciciocontable',
            name='ano',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Año'),
        ),
        migrations.RunPython(set_ano_from_inicio, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='ejerciciocontable',
            name='ano',
            field=models.PositiveSmallIntegerField(verbose_name='Año'),
        ),
    ]
