from rest_framework import serializers
from .models import *


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'start_date'
            'end_date'
            'updated_at'
        )


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )


class SubscriptionListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(
        source="subscription_type.title",
        read_only=True
    )
    limit_in_month = serializers.CharField(
        source="subscription_type.limit_in_month",
        read_only=True
    )
    book_name = serializers.CharField(
        source="item.book_name",
        read_only=True
    )
    class Meta:
        model = Subscription
        fields = (
            'customer',
            'type',
            'limit_in_month',
            'book_name',
            'coupon',
            'total_cost',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
            'status',
            'percentage',
            'days_remaining',
            'is_valid',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )
