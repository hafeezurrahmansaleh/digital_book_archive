from datetime import datetime, date, timedelta
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from archive.models import BookDetails
from subscription.models import Subscription, PaymentDetails
from user_profile.models import *
# from django.db.models.lookups import MonthTransform as Month, YearTransform as Year
from django.db.models.functions import TruncMonth as Month, TruncYear as Year
from django.db.models import Count, Q
import calendar
from .serializers import CustomerListSerializer, BookListSerializer, SubscriptionSerializer, PaymentSerializer
from django.db import connection


# class findUser(APIView):
#     def get(self, request):
#         user =

def isDateValid(date):
    correctDate = None
    try:
        newDate = datetime.fromisoformat(date)
        correctDate = True
    except ValueError:
        correctDate = False
    finally:
        return correctDate


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

        subscriptionOverview = [
                        {
                            "month": "Jan",
                            "subscription": 0
                        },
                        {
                            "month": "Feb",
                            "subscription": 0
                        },
                        {
                            "month": "Mar",
                            "subscription": 0
                        },
                        {
                            "month": "Apr",
                            "subscription": 0
                        },
                        {
                            "month": "May",
                            "subscription": 0
                        },
                        {
                            "month": "Jun",
                            "subscription": 0
                        },
                        {
                            "month": "Jul",
                            "subscription": 0
                        },
                        {
                            "month": "Aug",
                            "subscription": 0
                        },
                        {
                            "month": "Sep",
                            "subscription": 0
                        },
                        {
                            "month": "Oct",
                            "subscription": 0
                        },
                        {
                            "month": "Nov",
                            "subscription": 0
                        },
                        {
                            "month": "Dec",
                            "subscription": 0
                        }
                    ]
        subscriptions = Subscription.objects.filter(created_at__year=year).values('created_at__month').annotate(total=Count('created_at__month')).order_by('total')
        # print(subscriptionOverview)
        for sub in subscriptions:
            subscriptionOverview[int(sub["created_at__month"])-1]["subscription"] = int(sub["total"])
            # print(int(t["created_at__month"]))
        # print(subscriptionOverview)

        # subscriptionOverview = []
        # for month_idx in range(1, last_month+1):
        #     # print(calendar.month_name[month_idx])
        #     perMonthSubs = Subscription.objects.filter(created_at__month=month_idx, created_at__year=year).count()
        #     subscriptionOverview.append({'month': calendar.month_abbr[month_idx], 'subscription': perMonthSubs})

        return Response(subscriptionOverview)


class CustomerList(APIView):
    def get(self, request):
        # month = self.request.GET.get('month', date.today().month)
        # year = self.request.GET.get('year', date.today().year)
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            customers = CustomerProfile.objects.filter(Q(subscription__status='Active') | Q(subscription__status=None),
                                                       created_at__range=[start, end]).values(
                'full_name', 'email', 'phone', 'created_at', 'subscription__status', 'pk').distinct()
            # payments = PaymentDetails.objects.filter(created_at__range=[start, end])
            serializer = CustomerListSerializer(customers, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')

        # customers = CustomerProfile.objects.filter(Q(subscription__status='Active') | Q(subscription__status=None), created_at__month=month, created_at__year=year).values('full_name', 'email', 'phone', 'created_at', 'subscription__status', 'pk').distinct()
        #
        # serializer = CustomerListSerializer(customers, many=True)

        # cursor = connection.cursor()
        # customerList = []
        # cursor.execute(f'SELECT DISTINCT user_profile_customerprofile.id, user_profile_customerprofile.full_name, user_profile_customerprofile.email, user_profile_customerprofile.phone, subscription_subscription.status FROM user_profile_customerprofile LEFT JOIN subscription_subscription ON user_profile_customerprofile.id = subscription_subscription.customer_id AND subscription_subscription.status="Active" WHERE strftime("%m", user_profile_customerprofile.created_at) = "{month}" AND strftime("%Y", user_profile_customerprofile.created_at) = "{year}"')
        # for row in cursor:
        #     customerList.append({"full_name": row[1], "email": row[2], "phone": row[3], "status": row[4]})

        # return Response(serializer.data)
        # return Response(customerList)


class BookList(APIView):
    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            books = BookDetails.objects.filter(created_at__range=[start, end])
            serializer = BookListSerializer(books, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')
        # books = BookDetails.objects.all()
        # serializer = BookListSerializer(books, many=True)
        #
        # return Response(serializer.data)


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


class PaymentList(APIView):
    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            payments = PaymentDetails.objects.filter(created_at__range=[start, end])
            serializer = PaymentSerializer(payments, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')