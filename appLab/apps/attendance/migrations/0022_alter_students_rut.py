# Generated by Django 5.0.2 on 2024-07-29 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_students_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='rut',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='rut'),
        ),
    ]
