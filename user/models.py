from django.db import models
from xauth import models as xmodels


class User(xmodels.AbstractUser):
    pass
