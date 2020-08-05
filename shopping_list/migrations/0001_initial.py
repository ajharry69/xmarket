# Generated by Django 3.0.8 on 2020-08-04 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('item_name', 'created_on', 'updated_on'),
            },
        ),
        migrations.CreateModel(
            name='PurchaseMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1)),
                ('unit', models.CharField(max_length=50)),
                ('shopping_list', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shopping_list.ShoppingList')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1)),
                ('unit', models.CharField(max_length=50)),
                ('shopping_list', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shopping_list.ShoppingList')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
