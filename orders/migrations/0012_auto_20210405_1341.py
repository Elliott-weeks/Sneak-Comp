# Generated by Django 3.1.7 on 2021-04-05 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20210404_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.address'),
        ),
    ]