# Generated by Django 5.0.2 on 2024-05-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_gives_date_out_alter_gives_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='is_back',
            field=models.BooleanField(default=False, verbose_name='Devuelto'),
        ),
        migrations.AlterField(
            model_name='gives',
            name='is_back',
            field=models.BooleanField(default=False, verbose_name='Devuelto'),
        ),
    ]
