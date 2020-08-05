import os
from hashlib import md5

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime


def article_media_content_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    author_id, article_id = instance.article.author.id, instance.article.id
    encoded_timestamped_id = f"{author_id}{article_id}{datetime.utcnow().timestamp()}".encode(
        encoding='utf8',
        errors='replace')
    hashed_timestamped_id = md5(encoded_timestamped_id).hexdigest()
    return os.path.join(f'articles/', f"{hashed_timestamped_id}.{ext}")


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=250, blank=False, null=False, )
    content = models.TextField(null=False, )
    publication_date = models.DateTimeField(default=timezone.now)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('publication_date', 'creation_time', 'update_time',)


class Media(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.FileField(upload_to=article_media_content_upload_path)


class Comments(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.CharField(max_length=250, )
    post_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
