from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    from_email = getattr(settings, 'EMAIL_HOST_USER')

    class Meta:
        db_table = 'tbl_users'
