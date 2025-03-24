from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
