from datetime import datetime, date
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from archive.models import BookDetails
from subscription.models import Subscription
from user_profile.models import *
# from django.db.models.lookups import MonthTransform as Month, YearTransform as Year
from django.db.models.functions import TruncMonth as Month, TruncYear as Year
from django.db.models import Count, Q
import calendar
from .serializers import UserProfileListSerializer, BookListSerializer, SubscriptionSerializer


class Summary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        total_booklist = BookDetails.objects.all().count()
        total_customer = CustomerProfile.objects.filter(is_active=True).count()
        total_subscription = Subscription.objects.filter(status='Active', end_date__gt=datetime.now().astimezone()).count()
        total_publisher = PublisherProfile.objects.all().count()
        return Response([
            {'title': 'Booklist', 'number': total_booklist},
            {'title': 'Customer', 'number': total_customer},
            {'title': 'Subscription', 'number': total_subscription},
            {'title': 'Publisher', 'number': total_publisher}
        ])

class SubscriptionChart(APIView):

    def get(self, request):
        year = self.request.GET.get('year', date.today().year)
        # print(type(date.today().year))
        # if int(year) == date.today().year:
        #     last_month = date.today().month
        # else:
        last_month = 12

        subscriptionOverview = []
        for month_idx in range(1, last_month+1):
            # print(calendar.month_name[month_idx])
            perMonthSubs = Subscription.objects.filter(created_at__month=month_idx, created_at__year=year).count()
            subscriptionOverview.append({'month': calendar.month_abbr[month_idx], 'subscription': perMonthSubs})

        return Response(subscriptionOverview)


class CustomerList(APIView):
    def get(self, request):
        # customers = CustomerProfile.objects.filter(is_active=True, )
        # serializer = UserProfileListSerializer(customers, many=True)

        # for test in CustomerProfile.objects.raw('SELECT * FROM user_profile_customerprofile LEFT JOIN subscription_subscription ON user_profile_customerprofile.id = subscription_subscription.customer_id'):
        # for test in Subscription.objects.raw(
        #         'SELECT DISTINCT id, customer_id FROM subscription_subscription WHERE status="Active"'):
        #     print(test)
        # "SELECT id FROM user_profile_customerprofile UNION SELECT DISTINCT customer_id FROM subscription_subscription WHERE status="Active""
        from django.db import connection
        cursor = connection.cursor()
        customerList = []
        cursor.execute('SELECT DISTINCT user_profile_customerprofile.id, user_profile_customerprofile.full_name, user_profile_customerprofile.email, user_profile_customerprofile.phone, subscription_subscription.status FROM user_profile_customerprofile LEFT JOIN subscription_subscription ON user_profile_customerprofile.id = subscription_subscription.customer_id AND subscription_subscription.status="Active"')
        for row in cursor:
            customerList.append({"full_name": row[1], "email": row[2], "phone": row[3], "status": row[4]})

        # return Response(serializer.data)
        return Response(customerList)


class BookList(APIView):
    def get(self, request):
        books = BookDetails.objects.all()
        serializer = BookListSerializer(books, many=True)

        return Response(serializer.data)

class PublisherList(APIView):
    def get(self, request):
        publisher = BookDetails.objects.all().values('publisher__name', 'publisher__email').annotate(total=Count('publisher')).order_by('total')
        print(publisher)
        # ransaction.objects.all().values('actor').annotate(total=Count('actor')).order_by('total')
        return Response(publisher)


class SubscriptionList(APIView):
    def get(self, request):
        activeSubscription = Subscription.objects.filter(status='Active')
        allSubscription = Subscription.objects.all()

        activeSerializer = SubscriptionSerializer(activeSubscription, many=True)
        allSerializer = SubscriptionSerializer(allSubscription, many=True)

        return Response({ 'activeSubscription': activeSerializer.data, 'allSubscription': allSerializer.data })

