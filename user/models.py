import os
from hashlib import md5

from PIL import Image
from django.db import models
from xauth import models as xmodels
from xauth.utils import valid_str


def resize_image(photo_path, height=250, width=250):
    if valid_str(photo_path):
        image = Image.open(photo_path)
        # resize only photos with height and width greater than 250
        if image.width > width or image.height > height:
            output_size = (width, height)
            image.thumbnail(output_size)
            image.save(photo_path)


def photo_upload_path(instance, photo):
    """
    creates an upload path for `photo` with `photo` renamed to hashed value of `instance.id`
    """
    ext = photo.split('.')[-1]
    encoded_id = f"{instance.id}".encode(encoding='utf8', errors='replace')
    hashed_id = md5(encoded_id).hexdigest()
    return os.path.join('images/profile/', f"{hashed_id}.{ext}")


class User(xmodels.AbstractUser):
    photo = models.ImageField(
        upload_to=photo_upload_path,
        null=True, blank=True, default=None,
    )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        photo_path = self.photo.path if self.photo else None
        # assert photo was uploaded and has a path
        resize_image(photo_path)
