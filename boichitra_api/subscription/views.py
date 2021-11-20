from django.db.models import Q
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)

from .serializers import *


class CreateSubscriptionView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateSubscriptionSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        user = self.request.user
        customer_profile = CustomerProfile.objects.get(user=user)
        subscription_list = Subscription.objects.filter(customer=customer_profile, status='Active',
                                                        end_date__gt=datetime.now().astimezone())
        if subscription_list.exists():
            subscription_list.update(status='Cancelled')
            # subscription_list.save()
        serializer.save(customer=customer_profile, status='Active')


class SubscriptionTypeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionTypeSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        subscription_types = SubscriptionType.objects.filter(is_active=True)
        return subscription_types


class MySubscriptionsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionListSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        customer_profile = CustomerProfile.objects.get(user=user)
        subscription_list = Subscription.objects.filter(customer=customer_profile,status = 'Active',end_date__gt=datetime.now().astimezone())
        # print(subscription_list[0].percentage)
        return subscription_list


class MySubscriptionsHistoryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionListSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        customer_profile = CustomerProfile.objects.get(user=user)
        subscription_list = Subscription.objects.filter(Q((~Q(status = 'Active') or Q(end_date__lt=datetime.now().astimezone()))),customer=customer_profile)
        # print(subscription_list[0].percentage)
        return subscription_list


