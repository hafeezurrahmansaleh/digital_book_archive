from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
# from django.contrib.auth.models import update_last_login


class ChangePasswordByEmailSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset
    """
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get("username"),
            'phone': attrs.get("phone"),
            'password': attrs.get("password")
        }

        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first(
        ) or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)


class EmailVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('is_verified',)


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class SendOTPConSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordCodeConfirmationSerializer(serializers.Serializer):
    """
    serializer for validating email and send code
    """
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


''' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Mobile OTP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password','username','is_customer','is_publisher','is_admin','is_staff')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id', 'phone', 'first_login')


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('password')
        password = attrs.get('phone')  #attrs.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                dt = datetime.today()  # Get timezone naive now

                # from django.db.models import DurationField, F, ExpressionWrapper
                # import datetime
                #
                # Race.objects.annotate(
                #     diff=ExpressionWrapper(F('end') - F('start'), output_field=DurationField())
                # ).filter(diff__gte=datetime.timedelta(5))

                seconds = dt.timestamp()
                valid_otp = PhoneOTP.objects.filter(phone=phone,otp=otp)
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and
    password reset(No login required but otp required)
    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview


class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

