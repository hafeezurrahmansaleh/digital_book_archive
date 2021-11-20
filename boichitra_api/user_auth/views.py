from django.shortcuts import render

# Create your views here.

from django.http import Http404
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from user_profile.models import *
from user_profile.serializers import *
from .serializers import *
# from customer_order.models import FoodOrder
from .models import *
from .serializers import VerifyEmailSerializer
from .verification import Verification
import random,math
import string
import hashlib


# Create your views here.

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# function to generate OTP
def generateOTP(otpLength = 4):

    """Generate a random OTP of fixed length """
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(otpLength):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class CustomerSignUp(generics.CreateAPIView):
    """
    endpoint for customer sign up
    """
    permission_classes = (AllowAny,)
    serializer_class = CreateCustomerSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        number_code = "{}".format(randomString(10))
        code = hashlib.md5(number_code.encode())
        new_code = code.hexdigest()
        otp = generateOTP(4)
        ins = serializer.save(is_active=False,password=otp)
        EmailVerificationCode.objects.create(
            user=ins,
            code=new_code
        )
        Verification().send_email_verification_code(email, new_code)
        print('code sent')


class VerifyEmail(generics.UpdateAPIView):
    """
    endpoint for verify email address
    """
    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer
    queryset = EmailVerificationCode.objects.all()

    def get_object(self):
        return

    def perform_update(self, serializer):
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            instance = EmailVerificationCode.objects.get(
                user__user__email=email,
                code=code,
                is_verified=False
            )
        except EmailVerificationCode.DoesNotExist:
            raise ValidationError('Code Expired')
        instance.is_verified = True
        instance.save()

        user_instance = User.objects.get(username=instance.user.user.username)
        user_instance.is_active = True
        user_instance.save()


class ChangePassword(APIView):
    """
    end point for changing user password
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *arg, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            response = {}
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"errors": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response["success"] = "Password updated successfully"
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SendPasswordResetCode(generics.CreateAPIView):
    """
    end point for sending password reset email
    """
    permission_classes = (AllowAny,)
    serializer_class = SendOTPConSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        try:
            instance = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise ValidationError('No active account found with this email')
        number_code = "{}".format(randomString(10))
        code = hashlib.md5(number_code.encode())
        new_code = code.hexdigest()

        ForgetPasswordCode.objects.create(
            user=instance,
            code=new_code
        )
        Verification().send_password_reset_email(email, new_code)


class ResetPassword(generics.RetrieveUpdateAPIView):
    """
    endpoint for verifying password code
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer
    queryset = User.objects.all()
    lookup_fields = ['email', 'code']

    def get_object(self):
        email = self.kwargs.get('email')
        code = self.kwargs.get('code')
        try:
            instance = ForgetPasswordCode.objects.get(
                user__email=email,
                code=code,
                is_verified=False
            )
            instance.is_verified = True
            instance.save()
        except ForgetPasswordCode.DoesNotExist:
            raise ValidationError('Invalid code')

    def perform_update(self, serializer):
        email = self.kwargs.get('email')
        instance = User.objects.get(
            email=email
        )
        instance.set_password(serializer.validated_data['new_password'])
        instance.save()


###################################################################################################################
########################################### Mobile Authentication #################################################
###################################################################################################################

from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from .utils import phone_validator, password_generator, otp_generator
from .serializers import (CreateUserSerializer, ChangePasswordSerializer,
                          UserSerializer, LoginUserSerializer, ForgetPasswordSerializer)
# from accounts.models import User, PhoneOTP
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests

from rest_framework.views import APIView

# class LogoutView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, format=None):
#         request._auth.delete()
#         user_logged_out.send(sender=request.user.__class__,
#                              request=request, user=request.user)
#         return Response(None, status=status.HTTP_204_NO_CONTENT)


class LoginAPI(KnoxLoginView):
    ''' User login api view '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None:
            user.first_login = True
            user.save()

        elif user.first_login:
            user.first_login = False
            user.save()

        login(request, user)
        return super().post(request, format=None)


class UserAPI(generics.RetrieveAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPI(generics.UpdateAPIView):
    """
    Change password endpoint view
    """
    # authentication_classes = (TokenAuthentication,)
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, queryset=None):
        """
        Returns current logged in user instance
        """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('password_1')):
                return Response({
                    'status': False,
                    'current_password': 'Does not match with our data',
                }, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('password_2'))
            self.object.password_changed = True
            self.object.save()
            return Response({
                "status": True,
                "detail": "Password has been successfully changed.",
            })

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


def send_otp(phone,app_key):
    """
    This is an helper function to send otp to session stored phones or
    passed phone number as argument.
    """

    if phone:

        key = otp_generator()
        phone = str(phone).replace('+','')
        otp_key = str(key)
        print(phone)
        link = f'https://smsplus.sslwireless.com/api/v3/send-sms?api_token=somikoron.com-ea900be5-6c20-41af-a05a-ee9bc50a3c08&sid=SOMIKORONNONBRAND&msisdn={phone}&csms_id=513&sms=<%23> Your code is: {otp_key}  -বইচিত্র \n{app_key}'

        # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'

        result = requests.get(link, verify=False)
        print(result.json())
        if result.json()['status'] == 'SUCCESS':
            return otp_key
        else:
         return False
    else:
        return False


def send_otp_forgot(phone,app_key):
    if phone:
        key = otp_generator()
        phone = str(phone).replace('+','')
        otp_key = str(key)
        user = get_object_or_404(User, phone__iexact=phone)
        # if user.name:
        #     name = user.name
        # else:
        #     name = phone

        link = f'https://smsplus.sslwireless.com/api/v3/send-sms?api_token=somikoron.com-ea900be5-6c20-41af-a05a-ee9bc50a3c08&sid=SOMIKORONNONBRAND&sms=<#> Your code is: {otp_key}  -বইচিত্র\n{app_key}&msisdn={phone}&csms_id=513'
        # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfgs&templatename=Wisfrags&var1={name}&var2={otp_key}'

        result = requests.get(link, verify=False)
        print(result)

        return otp_key
    else:
        return False


############################################################################################################################################################################################
################################################################################################################################################################


class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    serializer_class = SendOTPConSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        app_key = request.data.get('app_key')
        # logged_otp = PhoneOTP.objects.filter(phone=phone_number,logged=True)
        if phone_number and len(phone_number)>=10:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            # if user.exists():
            #     return Response({'status': False,
            #                      'is_existing_user': True,
            #                      'detail': 'Phone Number already exists! Please try forgot password option'})
                # logic to send the otp and store the phone number and that otp in table.

            # This section should be removed later
            # if logged_otp.exists():
            #     return Response({'status': False,
            #                      'is_existing_user': True,
            #                      'detail': 'User already logged in'})

            otp = send_otp(phone,app_key)
            print(phone, otp, app_key)
            if otp:
                otp = str(otp)
                count = 0
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    count = old.first().count+1
                    old_ins = PhoneOTP.objects.filter(phone__iexact=phone).update(count=count, otp=otp)

                    print(old.first().count)
                    # old.first().count = count + 5
                    # old.first().otp = otp
                    # old.first().update(otp = otp, count = count+1)

                else:
                    count = count + 1

                    PhoneOTP.objects.create(
                        phone=phone,
                        otp=otp,
                        count=count

                    )
                if count > 1000:
                    return Response({
                        'status': False,
                        'is_existing_user': False,
                        'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                    })
            else:
                return Response({
                    'status': 'False','is_existing_user': False, 'detail': "OTP sending error. Please try after some time."
                })

            return Response({
                'status': True,'is_existing_user': False, 'detail': 'Otp has been sent successfully.'
            })
        else:
            return Response({
                'status': 'False','is_existing_user': False, 'detail': "Phone number is invalid. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            print(old)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    user = User.objects.filter(phone__iexact=phone)
                    if user.exists():
                        return Response({
                            'status': True,
                            'detail': 'OTP matched and user already exists, please proceed to login'
                        })
                    else:
                        Temp_data = {'phone': phone, 'password': phone, 'username':phone, 'is_customer':1}
                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save(is_customer = True )
                        user.save()
                        print(user)

                        usr_grp = Group.objects.get(name__iexact='customer')
                        user.groups.add(usr_grp)

                        user_new = User.objects.get(phone__iexact=phone)
                        user_id = user_new.id
                        print(user_id)

                        Temp_profile_data = {'phone': phone, 'email': None, "full_name": None}
                        serializer = CreateCustomerProfileSerializer(data=Temp_profile_data)
                        serializer.is_valid(raise_exception=True)
                        customer = serializer.save(user=user)
                        customer.save()

                        return Response({
                            'status': True,
                            'detail': 'OTP matched and new user created, please proceed to login'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not received in Post request'
            })


class Register(APIView):

    '''
    Takes phone and a password and creates a new user only if otp was verified and phone is new
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        full_name = request.data.get('name', False)
        email = request.data.get('email', False)

        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    if old.logged:

                        Temp_data = {'phone': phone, 'password': password, 'username':phone, 'is_customer':1}

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save(is_customer = True )
                        user.save()
                        print(user)

                        usr_grp = Group.objects.get(name__iexact='customer')
                        user.groups.add(usr_grp)

                        user_new = User.objects.get(phone__iexact=phone)
                        user_id = user_new.id
                        print(user_id)
                        Temp_profile_data = {'phone': phone, 'email': email, "full_name":full_name}
                        serializer = CreateCustomerProfileSerializer(data=Temp_profile_data)
                        serializer.is_valid(raise_exception=True)
                        customer = serializer.save(user=user)
                        customer.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Congrats, user has been created successfully.'
                        })


                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number not recognised. Kindly request a new otp with this number'
                    })

        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or password was not received in Post request'
            })


class ValidatePhoneForgot(APIView):
    '''
    Validate if account is there for a given phone number and then send otp for forgot password reset'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        app_key = request.data.get('app_key')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                otp = send_otp_forgot(phone,app_key)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        k = old.count
                        if k > 10:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly contact our customer care or try with different number'
                            })
                        old.count = k + 1
                        old.otp = otp
                        old.forgot = True
                        old.save()
                        return Response(
                            {'status': True, 'detail': 'OTP has been sent for password reset. Limits about to reach.'})

                    else:
                        count = count + 1

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            count=count,
                            forgot=True,

                        )
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})

                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number not recognised. Kindly try a new account for this number'
                })

# class ValidatePhoneSendOTP(APIView):
#     '''
#     This class view takes phone number and if it doesn't exists already then it sends otp for
#     first coming phone numbers'''

#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone')
#         if phone_number:
#             phone = str(phone_number)
#             user = User.objects.filter(phone__iexact = phone)
#             if user.exists():
#                 return Response({'status': False, 'detail': 'Phone Number already exists'})
#                  # logic to send the otp and store the phone number and that otp in table.
#             else:
#                 otp = send_otp(phone)
#                 print(phone, otp)
#                 if otp:
#                     otp = str(otp)
#                     count = 0
#                     old = PhoneOTP.objects.filter(phone__iexact = phone)
#                     if old.exists():
#                         count = old.first().count
#                         old.first().count = count + 1
#                         old.first().save()

#                     else:
#                         count = count + 1

#                         PhoneOTP.objects.create(
#                              phone =  phone,
#                              otp =   otp,
#                              count = count

#                              )
#                     if count > 7:
#                         return Response({
#                             'status' : False,
#                              'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
#                         })
#                 else:
#                     return Response({
#                                 'status': 'False', 'detail' : "OTP sending error. Please try after some time."
#                             })

#                 return Response({
#                     'status': True, 'detail': 'Otp has been sent successfully.'
#                 })
#         else:
#             return Response({
#                 'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
#             })


class ForgotValidateOTP(APIView):
    '''
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset  the forgotted password

    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                if old.forgot == False:
                    return Response({
                        'status': False,
                        'detail': 'This phone have not send valid otp for forgot password. Request a new otp or contact help centre.'
                    })

                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, please move forward to reset password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            })


class ForgetPasswordChange(APIView):
    '''
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp = request.data.get("otp", False)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact=phone) & Q(otp__iexact=otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone': phone,
                        'password': password
                    }
                    user_obj = get_object_or_404(User, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data=post_data)
                    serializer.is_valid(raise_exception=True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Password changed successfully. Please Login'
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Post request have parameters missing.'
            })


class tmpLogout(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        po = PhoneOTP.objects.filter(phone = phone).update(logged=False)
        # po.save()
        return Response({
            'status': True,
            'detail': 'User logged out successfully.'
        })