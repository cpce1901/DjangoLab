# Generated by Django 5.0.2 on 2024-05-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_gives_is_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='habilitado'),
        ),
    ]