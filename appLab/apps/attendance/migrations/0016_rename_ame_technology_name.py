# Generated by Django 5.0.2 on 2024-07-22 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_technology_remove_topicenabled_tecnologic_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technology',
            old_name='ame',
            new_name='name',
        ),
    ]
