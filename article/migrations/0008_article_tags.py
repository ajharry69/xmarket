# Generated by Django 3.1 on 2020-08-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_media_content_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.JSONField(default=[], null=True),
        ),
    ]
