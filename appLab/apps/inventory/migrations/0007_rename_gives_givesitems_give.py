# Generated by Django 5.0.2 on 2024-02-09 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_gives_student_giveitem_givesitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='givesitems',
            old_name='gives',
            new_name='give',
        ),
    ]
