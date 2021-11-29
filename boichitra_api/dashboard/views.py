import json
from datetime import datetime, date, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from subscription.models import Subscription, PaymentDetails
from user_profile.models import *
from user_auth.models import User
from django.db.models import Count, Q
from .serializers import CustomerListSerializer, BookListSerializer, PaymentSerializer, \
    UserSerializer, ActiveSubscriptionSerializer, AllSubscriptionSerializer
import time


def isDateValid(date):
    correctDate = None
    try:
        newDate = datetime.fromisoformat(date)
        correctDate = True
    except ValueError:
        correctDate = False
    finally:
        return correctDate


class getUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        body_unicode = self.request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_id = body["user_id"]
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        # time.sleep(60)

        return Response(serializer.data)


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
    permission_classes = (IsAuthenticated,)

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
        for sub in subscriptions:
            subscriptionOverview[int(sub["created_at__month"])-1]["subscription"] = int(sub["total"])

        return Response(subscriptionOverview)


class CustomerList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            customers = CustomerProfile.objects.filter(Q(subscription__status='Active') | Q(subscription__status=None),
                                                       created_at__date__range=[start, end]).values(
                'full_name', 'email', 'phone', 'created_at', 'subscription__status', 'pk').distinct()
            serializer = CustomerListSerializer(customers, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')



class BookList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            books = BookDetails.objects.filter(created_at__date__range=[start, end])
            serializer = BookListSerializer(books, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')


class PublisherList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        publisher = PublisherProfile.objects.all().values('name', 'email').annotate(total=Count('book_publisher__id')).order_by('total')
        return Response(publisher)


class SubscriptionList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start

            activeSubscription = Subscription.objects.filter(status='Active', created_at__date__range=[start, end])
            allSubscription = CustomerProfile.objects.filter(~Q(subscription__status=None)).values('full_name', 'subscription__subscription_type__title', 'subscription__total_cost', 'subscription__start_date', 'subscription__end_date', 'subscription__status')

            activeSerializer = ActiveSubscriptionSerializer(activeSubscription, many=True)
            allSerializer = AllSubscriptionSerializer(allSubscription, many=True)

            return Response({'activeSubscription': activeSerializer.data, 'allSubscription': allSerializer.data})
        else:
            return Response('Invalid Date')



class PaymentList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start = self.request.GET.get('startDate')
        end = self.request.GET.get('endDate')

        if isDateValid(start) and isDateValid(end):

            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                start, end = end, start
            payments = PaymentDetails.objects.filter(created_at__date__range=[start, end])
            serializer = PaymentSerializer(payments, many=True)

            return Response(serializer.data)
        else:
            return Response('Invalid Date')