# Generated by Django 5.0.2 on 2024-07-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0020_teams_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='rut',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='rut'),
        ),
    ]
