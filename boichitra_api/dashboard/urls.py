from django.urls import path
from dashboard import views

urlpatterns = [
    path('summary/', views.Summary.as_view()),
    path('SubscriptionChart/', views.SubscriptionChart.as_view()),
    path('customers/', views.CustomerList.as_view()),
    path('books/', views.BookList.as_view()),
    path('publishers/', views.PublisherList.as_view()),
    path('subscriptions/', views.SubscriptionList.as_view())
]