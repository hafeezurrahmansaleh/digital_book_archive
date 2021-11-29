from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import models

# Create your models here.
from archive.models import BookDetails
from user_profile.models import CustomerProfile


class SubscriptionType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    sub_title = models.CharField(max_length=128, null=True, blank=True)
    limit_in_month = models.IntegerField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        blank=True
    )
    condition = models.TextField(
        max_length=1000,
        null=True,
        blank=True
    )
    priority = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '--' + str(self.limit_in_month) + 'month(s)'

    class Meta:
        ordering = ('priority', '-created_at')


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('Percentage', 'Percentage'),
        ('Amount', 'Amount'),
    )
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    percentage = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    limit_per_user = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    priority = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('priority', '-created_at')

    def __str__(self):
        return self.code


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Suspended', 'Suspended'),
        ('Cancelled', 'Cancelled'),
        ('Expired', 'Expired'),
    )
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscription'
    )
    subscription_type = models.ForeignKey(
        SubscriptionType,
        on_delete=models.SET_NULL,
        null=True
    )
    item = models.ForeignKey(
        BookDetails,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='Active',
        max_length=10
    )

    # slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.customer.full_name + '--' + self.subscription_type.title + '--' + self.status

    @property
    def percentage(self):
        delta = self.end_date - self.start_date.astimezone()
        total_days = delta.days
        delta1 = datetime.now().astimezone() - self.start_date
        days_gone = delta1.days
        print(delta.days)
        percentage = (days_gone / total_days) * 100
        return percentage

    @property
    def days_remaining(self):
        delta1 = self.end_date - datetime.now().astimezone()
        days_remaining = delta1.days
        return days_remaining

    @property
    def is_valid(self):
        if self.end_date.astimezone() > datetime.now().astimezone() and self.status == 'Active':
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.total_cost = self.subscription_type.cost
        self.start_date = datetime.now()
        self.end_date = self.start_date + relativedelta(
            months=self.subscription_type.limit_in_month)  # datetime.strptime(self.start_date, "%Y-%m-%d")+timedelta(months=10)
        super(Subscription, self).save(*args, **kwargs)


class PaymentDetails(models.Model):
    id = models.AutoField(primary_key=True)
    PAYMENT_METHOD_CHOICES = (
        ('BKASH', 'BKASH'),
        ('ROCKET', 'ROCKET'),
        ('CARD', 'CARD'),
        ('CASHON', 'CASHON'),
        ('SSLCOMMERZ', 'SSLCOMMERZ'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Payment is pending'),
        ('PAID', 'Payment received'),
        ('PARTIAL', 'Partial payment received'),
        ('FAILED', 'Payment Failed'),
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='paymentDetails'
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=70, null=True, blank=True)
    is_failed = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.amount_paid is None or self.amount_paid is 0:
    #         self.amount_paid = self.order.order_total
    #     if self.payment_status == 'FAILED':
    #         self.is_failed = True
    #     super(PaymentDetails, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.id) + ' ' + self.payment_method + ' ' + self.payment_status