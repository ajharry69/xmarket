# Generated by Django 3.1 on 2020-08-14 12:58

import article.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20200805_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='content_thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=article.models.article_media_content_thumbnail_upload_path),
        ),
    ]
