# Generated by Django 5.0.2 on 2024-05-06 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_items_is_back_alter_gives_is_back'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gives',
            name='is_back',
        ),
    ]
