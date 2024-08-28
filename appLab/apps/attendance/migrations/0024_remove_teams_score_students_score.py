# Generated by Django 5.0.2 on 2024-07-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0023_alter_teams_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='score',
        ),
        migrations.AddField(
            model_name='students',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='Nota'),
        ),
    ]