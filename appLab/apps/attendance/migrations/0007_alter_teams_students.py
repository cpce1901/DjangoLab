# Generated by Django 5.0.2 on 2024-03-12 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_remove_classes_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='students',
            field=models.ManyToManyField(to='attendance.students', verbose_name='Estudiantes'),
        ),
    ]
