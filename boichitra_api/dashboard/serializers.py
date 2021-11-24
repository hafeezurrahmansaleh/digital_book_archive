from rest_framework import serializers

from archive.models import BookDetails
from subscription.models import Subscription, PaymentDetails
from user_profile.models import CustomerProfile


class CustomerListSerializer(serializers.ModelSerializer):
    subscription__status = serializers.CharField(
        # source="subscription.status",
        read_only=True
    )
    class Meta:
        model = CustomerProfile
        fields = ('full_name', 'email', 'phone', 'created_at', 'subscription__status')


class BookListSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(
        source="publisher.name",
        read_only=True
    )
    author_name = serializers.CharField(
        source="author.name",
        read_only=True
    )
    class Meta:
        model = BookDetails
        fields = ('book_name', 'author_name', 'publisher_name', 'rating')


class SubscriptionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.full_name",
        read_only=True
    )
    subscription_title = serializers.CharField(
        source="subscription_type.title",
        read_only=True
    )
    start_date = serializers.DateTimeField(format="%d-%m-%Y")
    end_date = serializers.DateTimeField(format="%d-%m-%Y")
    class Meta:
        model = Subscription
        fields = ('customer_name', 'subscription_title', 'total_cost', 'start_date', 'end_date')


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.full_name",
        read_only=True
    )
    class Meta:
        model = PaymentDetails
        fields = ('customer_name', 'payment_method', 'payment_status', 'amount_paid', 'transaction_id', 'is_failed')