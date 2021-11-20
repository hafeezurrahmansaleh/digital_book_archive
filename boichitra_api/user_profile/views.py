from django.shortcuts import render
from django.db import models
# Create your views here.
from django.http import Http404
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import get_object_or_404
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
    IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
)
from .permissions import IsOwnerOrReadOnly
from .models import *
from .serializers import *
from .owners import SectionOwner

User = django.contrib.auth.get_user_model()


# Create your views here.


class PublisherList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PublisherProfileSerializer
    queryset = PublisherProfile.objects.all()


# all Publisher related profile
class PublisherProfileDetail(generics.RetrieveUpdateAPIView):
    """
    endpoint for viewing logged Publisher
    user id should be pass as parameter
    """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PublisherProfileUpdateSerializer
    queryset = PublisherProfile.objects.all()
    lookup_field = 'user'


# all Restaurant related profiles


# all customer profile related class
class CustomerProfileCreate(generics.CreateAPIView):
    """
    endpoint for creating customer profile
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        querydata = UserRole.objects.filter(user=user, role_name='publisher')
        customerdata = CustomerProfile.objects.filter(user=user)
        # if user is superuser
        if user.is_superuser:
            raise ValidationError(
                'Superuser can not create a customer profile'
            )
        elif querydata.exists():
            raise ValidationError(
                'Publisher can not create a customer profile')
        elif customerdata.exists():
            raise ValidationError('Customer profile already exists')
        else:
            serializer.save(user=user)


class CustomerProfileDetail(generics.RetrieveUpdateAPIView):
    """
    endpoint for retrieve update and delete customer profile
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            raise ValidationError('This section is for customer only')
        return SectionOwner().is_customer(user)


class ViewUserProfile(generics.RetrieveAPIView):
    """
    endpoint for viewing user(customer,publisher profile)
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


"""
view user data
"""


class UserDataDetail(generics.RetrieveAPIView):
    """
    endpoint for retrieving all user data data from user table
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class WishlistCreateView(generics.CreateAPIView):
    """
    endpoint for creating wishlist
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistItemSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        customer_profile = CustomerProfile.objects.get(user=self.request.user)
        wishlists = Wishlist.objects.filter(customer=customer_profile)
        if wishlists.exists():
            wishlist = wishlists[0]
        else:
            wishlist = Wishlist.objects.create(customer=customer_profile)

        book_id = self.request.data.get('book', False)
        book = BookDetails.objects.get(pk=book_id)
        if WishlistItems.objects.filter(wishlist=wishlist, book_id=book_id).exists():
            raise ValidationError('This book is already in wishlist')

        else:
            print(wishlist)
            serializer.save(book=book)


class WishlistDeleteView(generics.DestroyAPIView):
    """
    endpoint for creating wishlist
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistItemSerializer
    authentication_classes = (TokenAuthentication,)

    def delete(self, request, *args, **kwargs):
        customer_profile = CustomerProfile.objects.get(user=self.request.user)
        wishlist = get_object_or_404(Wishlist, customer=customer_profile)
        book_id = self.request.data.get('book', False)
        # if WishlistItems.objects.filter(wishlist=wishlist, book_id=book_id).exists():
            # raise ValidationError('This section is for customer only')
        item = get_object_or_404(WishlistItems,wishlist = wishlist,book_id = book_id)
        item.delete()
        return Response("Item removed", status=status.HTTP_204_NO_CONTENT)


class MyWishlistView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistItemSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        customer_profile = CustomerProfile.objects.get(user=user)
        my_wishlist = WishlistItems.objects.filter(wishlist__customer=customer_profile)
        return my_wishlist