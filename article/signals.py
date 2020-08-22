import os
import threading

from django.db.models import F
from django.db.models.signals import post_save, post_delete

from article import models


def on_flag_post_saved(sender, instance, created, **kwargs):
    if created:
        article = instance.article
        article.flag_count = F('flag_count') + 1
        article.save()
        article.refresh_from_db()


def on_flag_post_delete(sender, instance, **kwargs):
    article = instance.article
    article.flag_count = F('flag_count') - 1
    article.save()
    article.refresh_from_db()


def on_media_post_saved(sender, instance, created, **kwargs):
    if created:
        threading.Thread(target=instance.generate_thumbnail).start()


def on_media_post_delete(sender, instance, **kwargs):
    def delete():
        os.remove(instance.content.path)
        os.remove(instance.content_thumbnail.path)

    threading.Thread(target=delete).start()


post_save.connect(on_media_post_saved, models.Media, dispatch_uid='media01-post-save')
post_delete.connect(on_media_post_delete, models.Media, dispatch_uid='media02-post-delete')
post_save.connect(on_flag_post_saved, models.Flags, dispatch_uid='flag01-post-save')
post_delete.connect(on_flag_post_delete, models.Flags, dispatch_uid='flag02-post-delete')
