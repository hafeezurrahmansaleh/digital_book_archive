import django.contrib.auth
from django.conf import settings
from django.db import models
# from user_auth.models import importUser
from archive.models import BookDetails

User = settings.AUTH_USER_MODEL
# User = django.contrib.auth.get_user_model()
from django.utils.translation import gettext_lazy as _
# Create your models here.


# class User(AbstractUser):
#     phone = models.CharField(_('phone number'), max_length=150, blank=True, unique=True)  # added by saleh
#     first_login = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.phone


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    about_author = models.TextField(null=True, blank=True)

    def natural_key(self):
        return (self.name)


class CustomerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_user'
    )
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    level_of_study = models.CharField(max_length=200, null=True, blank=True)
    area_of_interest = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    first_count = models.IntegerField(default=0,
                                      help_text='It is 0, if the user is totally new and 1 if the user has saved his standard once')

    def natural_key(self):
        return (self.full_name)

    def __str__(self):
        if self.full_name:
            rtn = self.user.phone + ' - ' + self.full_name
        else:
            rtn = self.user.phone
        return rtn


class PublisherProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='publisher_user'
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    about_publisher = models.CharField(max_length=1000, null=True, blank=True)
    # publisher_image = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to="publishers/",
    # )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class AdminProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin_user'
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # additional fields will be added later
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.full_name


class WishlistItems(models.Model):
    id = models.AutoField(primary_key=True)
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='wishlist_item'
    )
    book = models.ForeignKey(
        BookDetails,
        on_delete=models.CASCADE,
        related_name='wishlist_book'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.wishlist.customer_id) + ' - ' + self.book.book_name













