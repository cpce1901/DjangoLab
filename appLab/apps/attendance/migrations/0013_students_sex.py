# Generated by Django 5.0.2 on 2024-07-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_remove_students_class_name_students_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='sex',
            field=models.CharField(default='Hombre', max_length=16, verbose_name='Sexo'),
        ),
    ]
