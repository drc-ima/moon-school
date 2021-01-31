import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('username is required')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USER_TYPES = {
    ('AD', 'Administrator'),
    ('SAD', 'System Administrator'),
    ('SH', 'School Head'),
    ('ASH', 'Assistant School Head'),
    ('PU', 'Pupil User'),
    ('TU', 'Teacher'),
    ('CT', 'Class Teacher'),
    ('FO', 'Finance Officer'),
}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'),
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        _('Email address'),
        blank=True,
        null=True
    )
    first_name = models.CharField(_('First Name'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(_('Middle Name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True, null=True)
    account_id = models.CharField(_('Account Id'), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_('Active Status'), default=True)
    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_superuser = models.BooleanField(_('Super User Status'), default=False)
    slug = models.SlugField(blank=True, null=True, unique=True)
    profile = models.FileField(upload_to='profile/', blank=True, null=True)
    school_id = models.CharField(blank=True, null=True, max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, blank=True, null=True, unique=True)
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    user_type = models.CharField(_('User Type'), choices=USER_TYPES, max_length=255, blank=True,
                                 null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'user'
        ordering = ('-id', '-date_joined')
        db_table = 'user'

    def __str__(self):
        return f'{self.get_full_name()}'



