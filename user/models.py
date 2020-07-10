import os
from hashlib import md5

from PIL import Image
from django.db import models
from xauth import models as xmodels
from xauth.utils import valid_str


def resize_image(photo_path, height=450, width=450, square: bool = True):
    if valid_str(photo_path):
        image = Image.open(photo_path)
        smallest_dimen = min(width, height)
        smallest_img_dimen = min(image.width, image.height)
        resize_dimen = min(smallest_dimen, smallest_img_dimen)
        output_size = (resize_dimen, resize_dimen) if square else (width, height)
        image.thumbnail(output_size)
        image.save(photo_path)


def photo_upload_path(instance, photo):
    """
    creates an upload path for `photo` with `photo` renamed to hashed value of `instance.id`
    """
    ext = photo.split('.')[-1]
    id = instance.id
    encoded_id = f"{id if id else instance.username}".encode(encoding='utf8', errors='replace')
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
