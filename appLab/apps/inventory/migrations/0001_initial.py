# Generated by Django 5.0.2 on 2024-02-09 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_out', models.DateField(auto_now_add=True, verbose_name='Fecha de prestamos')),
                ('date_back', models.DateField(verbose_name='Fecha de devolución')),
                ('is_give', models.BooleanField(verbose_name='Entregado')),
                ('is_back', models.BooleanField(verbose_name='Devuelto')),
                ('observations', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Observaciones')),
                ('gives', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.materials', verbose_name='Prestamo')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='attendance.students', verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Prestamos',
                'verbose_name_plural': 'Prestamos',
            },
        ),
    ]