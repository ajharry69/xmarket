import os
import shutil
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


def article_media_content_thumbnail_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    file = instance.content.path.rsplit("/", 1)[1]
    return f'articles/thumbnails/{file.rsplit(".", 1)[0]}.{ext}'


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=250, blank=False, null=False, )
    content = models.TextField(null=False, )
    publication_date = models.DateTimeField(default=timezone.now)
    tags = models.JSONField(null=True, default=list)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('publication_date', 'creation_time', 'update_time',)

    def __str__(self):
        return self.headline


class Media(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.FileField(upload_to=article_media_content_upload_path)
    content_thumbnail = models.ImageField(
        upload_to=article_media_content_thumbnail_upload_path,
        null=True, blank=True, default=None,
    )

    @property
    def cache_path(self):
        return self.content.path.rsplit('/', 1)[0] + '/thumbnails/cache'

    def generate_thumbnail(self):
        from preview_generator.manager import PreviewManager
        cache_path = self.cache_path
        manager = PreviewManager(cache_path, create_folder=True)
        thumbnail = manager.get_jpeg_preview(self.content.path, width=150, height=80, force=True)
        with open(thumbnail, 'rb') as f:
            # save the thumbnail to the db
            self.content_thumbnail.save(thumbnail, f)
        # clean up thumbnail generation metadata
        shutil.rmtree(cache_path, ignore_errors=True)
        return thumbnail


class Comments(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.CharField(max_length=250, )
    post_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
