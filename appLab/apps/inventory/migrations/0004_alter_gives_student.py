# Generated by Django 5.0.2 on 2024-02-09 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('inventory', '0003_alter_gives_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gives',
            name='student',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='attendance.students', verbose_name='Estudiante'),
        ),
    ]
