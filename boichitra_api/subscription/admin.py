from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SubscriptionType)
admin.site.register(Coupon)
admin.site.register(Subscription)