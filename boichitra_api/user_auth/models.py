from django.db import models

from user_profile.models import CustomerProfile,PublisherProfile,Author,AdminProfile

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=17, unique=True)
    first_login = models.BooleanField(default=False)

    is_customer = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the customer site.'),
    )
    is_publisher = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the publisher site.'),
    )
    is_admin = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']


# Create your models here.
class EmailVerificationCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="email_verification"
    )
    code = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class ForgetPasswordCode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


''' <<<<<<<<<<<<<<<<<<< Mobile OTP >>>>>>>>>>>>>>>>>>>> '''

# from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

import random
import os
import requests


def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# def user_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user = instance)
# post_save.connect(user_created_receiver, sender = User)


class PhoneOTP(models.Model):
    # phone_regex = RegexValidator(regex=r'/^(?:\+88|88)?(01[3-9]\d{8})$/',
    #                              message="Phone number must be entered in the format: ")
    phone = models.CharField(max_length=17, unique=True) #validators=[phone_regex],
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if valid date otp forgot get successful')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
