# Generated by Django 3.1.7 on 2021-04-05 14:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitions', '0009_entries_valid_entry'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entries',
            new_name='Entrie',
        ),
    ]