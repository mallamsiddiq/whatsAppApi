from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .user_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    balance = models.FloatField(default = 0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    direct_contacts = models.ManyToManyField(
        'self',
        through='chat.DirectMessage',
        through_fields=('sender', 'recipient'),
        symmetrical=False,
        related_name='contact_of'
    )

    @property
    def get_direct_contacts(self):
        return self.direct_contacts.distinct()
    
    @property
    def slug_name(self):
        return slugify(self.email)
    

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
