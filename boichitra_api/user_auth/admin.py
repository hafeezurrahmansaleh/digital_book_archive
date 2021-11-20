from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import *
# Register your models here.


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    def user(self, obj):
        return obj.user.user.username

    list_display = ('user', 'code', 'is_verified')
    list_filter = ('is_verified',)


@admin.register(ForgetPasswordCode)
class ForgetPasswordCode(admin.ModelAdmin):
    def user(self, obj):
        return obj.username
    list_display = ('user', 'code', 'is_verified', 'created', 'updated')
    list_filter = ('is_verified',)

admin.site.register(PhoneOTP)
admin.site.register(Permission)
admin.site.register(User)

