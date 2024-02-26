# Generated by Django 5.0.2 on 2024-02-09 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Carrera',
                'verbose_name_plural': 'Carreras',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=32, verbose_name='Apellido')),
                ('rut', models.CharField(max_length=10, verbose_name='RUT')),
            ],
            options={
                'verbose_name': 'Estudiante',
                'verbose_name_plural': 'Estudiantes',
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Asignatura')),
                ('code', models.CharField(max_length=16, verbose_name='Codigo')),
                ('teacher', models.CharField(max_length=32, verbose_name='Profesor')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school', to='attendance.schools', verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Asignatura',
                'verbose_name_plural': 'Asignaturas',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_in', models.DateTimeField(auto_now_add=True, verbose_name='Ingreso')),
                ('time_inside', models.TimeField(verbose_name='Tiempo estimado de permanencia')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.students', verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Nombre')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_name', to='attendance.classes', verbose_name='Asignatura')),
                ('students', models.ManyToManyField(blank=True, to='attendance.students', verbose_name='Estudiantes')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
        ),
    ]
