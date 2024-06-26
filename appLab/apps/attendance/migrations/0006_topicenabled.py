# Generated by Django 5.0.2 on 2024-04-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_alter_tecnologicenabled_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicEnabled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Nombre')),
                ('score', models.SmallIntegerField(blank=True, null=True, verbose_name='Puntaje')),
            ],
            options={
                'verbose_name': 'Tipo Habilitador',
                'verbose_name_plural': 'Tipos Habilitador',
            },
        ),
    ]
