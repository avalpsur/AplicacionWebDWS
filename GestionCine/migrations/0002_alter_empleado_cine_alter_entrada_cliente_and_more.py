# Generated by Django 5.1.2 on 2024-10-31 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionCine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='cine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleados_cine', to='GestionCine.cine'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='cliente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entradas_cliente', to='GestionCine.cliente'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='proyeccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entradas_proyeccion', to='GestionCine.proyeccion'),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='sala',
            field=models.ManyToManyField(related_name='peliculas_sala', to='GestionCine.sala'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cliente',
            field=models.ManyToManyField(related_name='productos_cliente', to='GestionCine.cliente'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_proveedor', to='GestionCine.proveedor'),
        ),
        migrations.AlterField(
            model_name='proyeccion',
            name='pelicula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecciones_pelicula', to='GestionCine.pelicula'),
        ),
        migrations.AlterField(
            model_name='proyeccion',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecciones_sala', to='GestionCine.sala'),
        ),
        migrations.AlterField(
            model_name='sala',
            name='cine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salas_cine', to='GestionCine.cine'),
        ),
        migrations.AlterField(
            model_name='sala',
            name='empleado',
            field=models.ManyToManyField(related_name='salas_empleado', to='GestionCine.empleado'),
        ),
    ]