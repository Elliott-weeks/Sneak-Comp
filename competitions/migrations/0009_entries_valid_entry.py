# Generated by Django 3.1.7 on 2021-04-05 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0008_auto_20210405_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='valid_entry',
            field=models.BooleanField(default=False),
        ),
    ]
