# Generated by Django 5.0.4 on 2024-04-08 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('tipo_identificacion', models.CharField(max_length=20)),
                ('numero_identificacion', models.CharField(max_length=40)),
                ('correo_electronico', models.CharField(max_length=30)),
                ('celular', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=50)),
            ],
        ),
    ]
