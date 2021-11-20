from django.urls import path
from django.conf.urls import url
from user_auth import views
# from rest_framework_jwt.views import (
#     obtain_jwt_token,verify_jwt_token,refresh_jwt_token
# )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import CustomJWTSerializer
from knox import views as knox_views

urlpatterns = [
    path('auth/api-token-auth/',
         TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer)),
    path('auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/change-password/', views.ChangePassword.as_view()),
    path('auth/current-logged-user/', views.CurrentUserDetail.as_view()),
    # path('auth/customer-signup/', views.CustomerSignUp.as_view()),
    # path('auth/verify-email/', views.VerifyEmail.as_view()),
    # path('auth/send-password-reset-code/',
    #      views.SendPasswordResetCode.as_view()),
    # path(
    #     'auth/reset-password/<str:email>/<str:code>/',
    #     views.ResetPassword.as_view(),
    # ),


    path('auth/login/', views.LoginAPI.as_view()),
    path('auth/get-user-data/', views.UserAPI.as_view()),
    path('auth/change-password/', views.ChangePasswordAPI.as_view()),
    path('auth/send-signup-otp/', views.ValidatePhoneSendOTP.as_view()),
    path('auth/validate-signup-otp/', views.ValidateOTP.as_view()),
    path('auth/complete-signup/', views.Register.as_view()),
    path('auth/send-forgot-otp/', views.ValidatePhoneForgot.as_view()),
    path('auth/validate-forgot-otp/', views.ForgotValidateOTP.as_view()),
    path('auth/reset-password/', views.ForgetPasswordChange.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('auth/logout/', views.tmpLogout.as_view(), name='tmp_logout'),
]
