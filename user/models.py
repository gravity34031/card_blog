from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    avatar = ResizedImageField(_("profile avatar"), size=[150, 150], force_format='WEBP', quality=100, crop=['middle', 'center'], max_length=128, blank=True, null=True, upload_to='avatar')
