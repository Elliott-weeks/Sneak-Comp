# Generated by Django 3.1.7 on 2021-03-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
    ]
