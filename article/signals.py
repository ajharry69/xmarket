import os
import threading

from django.db.models.signals import post_save, post_delete

from article.models import Media


def on_media_post_saved(sender, instance, created, **kwargs):
    if created:
        threading.Thread(target=instance.generate_thumbnail).start()


def on_media_post_delete(sender, instance, created, **kwargs):
    def delete():
        os.remove(instance.content.path)
        os.remove(instance.content_thumbnail.path)

    threading.Thread(target=delete).start()


post_save.connect(on_media_post_saved, Media, dispatch_uid='media01')
post_delete.connect(on_media_post_delete, Media, dispatch_uid='media02')
