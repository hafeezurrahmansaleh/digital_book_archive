from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'limit_in_month', 'cost', 'priority')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'percentage', 'limit_per_user', 'valid_from', 'valid_to', 'is_active')
    search_fields = ['payment_method']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    def start_date_formated(self, obj):
        return obj.start_date.strftime("%Y-%m-%d %H:%M:%S")
    start_date_formated.short_description = 'Start Date'

    def end_date_formated(self, obj):
        return obj.end_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date_formated.short_description = 'End Date'

    list_display = ('customer', 'subscription_type', 'total_cost', 'start_date_formated', 'end_date_formated', 'status')
    search_fields = ['customer__full_name', 'subscription_type__title', 'start_date__startswith', 'status']


@admin.register(PaymentDetails)
class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('payment_method', 'payment_status', 'amount_paid', 'transaction_id', 'is_failed')
    search_fields = ['payment_method', 'payment_status', 'transaction_id']