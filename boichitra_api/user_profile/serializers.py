from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from drf_extra_fields.fields import Base64ImageField

from user_auth.serializers import EmailVerificationCodeSerializer
from drf_writable_nested import WritableNestedModelSerializer

from archive.serializers import BookDetailsSerializer


# User Role Serializer
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'  # ('is_rest_owner',)
        read_only_fields = ('id',)


# restaurant owner profile serializer
class PublisherProfileSerializer(serializers.ModelSerializer):
    restaurant_image = Base64ImageField(required=False)

    class Meta:
        model = PublisherProfile
        fields = '__all__'
        read_only_fields = ('id', 'created', 'udpated', 'user')


class PublisherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherProfile
        fields = '__all__'
        read_only_fields = (
            'id',
            'is_active',
            'created_at',
            'updated_at',
            'user'
        )


# class CustomerProfile Serializer
class CustomerProfileSerializer(serializers.ModelSerializer):
    # email_verification = EmailVerificationCodeSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'is_active',
            'created_at',
            'updated_at'
        )


# User Serializer used for owner


class UserSerializer(WritableNestedModelSerializer):
    user_role = UserRoleSerializer(read_only=True)
    customer_profile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'date_joined',
            'last_login',
            'user_role',
            'customer_profile',
            'is_active',
            'is_staff',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'id', 'date_joined', 'last_login', 'is_active', 'is_staff',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user_role = UserRoleSerializer(read_only=True)
    customer_profile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'date_joined',
            'last_login',
            'customer_profile',
            'user_role',
            'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'id', 'date_joined', 'last_login', 'is_active',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# this serializer only used for signup user with mobile number
class CustomerProfileForSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = (
            'email',
        )


class CreateCustomerSerializer(WritableNestedModelSerializer):
    # customer_profile = CustomerProfileForSignupSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            # 'password',
            # 'customer_profile'
        )
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user


class UserActiveDeactiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)


class CreateCustomerProfileSerializer(WritableNestedModelSerializer):
    # customer_profile = CustomerProfileForSignupSerializer(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = (
            'phone',
            'email',
            'user_id',
            'full_name',
        )
        # extra_kwargs = {'password': {'write_only': True}}


class WishlistItemSerializer(serializers.ModelSerializer):
    items = 'WishlistSerializer(read_only=True, many=True)'
    book = BookDetailsSerializer(read_only=True)

    class Meta:
        model = WishlistItems
        fields = '__all__'
        read_only_fields = (
            'id',
            'wishlist', 'wishlist_items', 'WishlistItems'
        )

    def create(self, validated_data):
        user = self.context.get('request', None).user.id
        print(user)
        customer_profile = CustomerProfile.objects.get(user_id=user)
        wishlists = Wishlist.objects.filter(customer=customer_profile)
        print(validated_data)
        if wishlists.exists():
            wishlist = wishlists[0]
        else:
            wishlist = Wishlist.objects.create(customer=customer_profile)
            validated_data['wishlist_id'] = wishlist

        wishlist_item = WishlistItems(
            book=validated_data['book'],
            wishlist=wishlist
        )
        wishlist_item.save()

        return wishlist_item


class WishlistSerializer(serializers.ModelSerializer):
    # items = WishlistItemSerializer(read_only=True, many=True)
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return obj.wishlist_item.book.book_name

    class Meta:
        model = Wishlist
        fields = (
            'id',
            'items',
        )
