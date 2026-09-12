from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ventas', '0006_alter_cotizacion_estado'),
        ('produccion', '0010_seed_categorias_materia_prima'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaTecnica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='1.0', max_length=20)),
                ('descripcion', models.TextField(blank=True)),
                ('metraje_tela_por_unidad', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('consumo_hilo_por_unidad', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('unidad_consumo_hilo', models.CharField(default='m', max_length=10)),
                ('tolerancia_porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('aprobada', models.BooleanField(default=False)),
                ('actualizada_en', models.DateTimeField(auto_now=True)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ficha_tecnica_produccion', to='produccion.productoterminado')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialFichaTecnica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_por_unidad', models.DecimalField(decimal_places=4, max_digits=10)),
                ('desperdicio_porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('observaciones', models.CharField(blank=True, max_length=255)),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiales', to='produccion.fichatecnica')),
                ('materia_prima', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produccion.materiaprima')),
            ],
        ),
        migrations.AddField(
            model_name='ordenproduccion',
            name='pedido_origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordenes_produccion', to='ventas.pedido'),
        ),
    ]
