# Generated by Django 5.0.2 on 2024-05-06 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_items_gives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gives',
            name='all_items',
        ),
        migrations.AddField(
            model_name='items',
            name='gives',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.gives'),
            preserve_default=False,
        ),
    ]
