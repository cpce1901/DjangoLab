# Generated by Django 5.0.2 on 2024-07-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0022_alter_students_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='Nota'),
        ),
    ]
