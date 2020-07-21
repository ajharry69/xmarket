# Generated by Django 3.0.8 on 2020-07-21 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1)),
                ('unit', models.CharField(max_length=50)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
