from django.urls import path
from subscription import views

urlpatterns = [
    path('my-subscription/', views.MySubscriptionsListView.as_view()),
    path('my-subscription-history/', views.MySubscriptionsHistoryView.as_view()),
    path('subscription-types/', views.SubscriptionTypeListView.as_view()),
    path('create-subscription/', views.CreateSubscriptionView.as_view()),
]