# Generated by Django 5.1 on 2024-08-21 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quotes',
            new_name='Quote',
        ),
    ]
