from django.urls import path
from user_profile import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # restaurant profile urls
    path('user-profile/view/<int:pk>/', views.ViewUserProfile.as_view()),
    path('publishers/', views.PublisherList.as_view()),
    path('publisher/<int:user>/', views.PublisherProfileDetail.as_view()),

    # customer urls
    path('customer-profile/update/', views.CustomerProfileDetail.as_view()),
    path('customer-profile/', views.CustomerProfileDetail.as_view()),

    # customer feedbacks
    # path('customer-feedback/', views.CustomerFeedbackCreate.as_view()),

    # orders
    # path('my-orders/', views.LoggedInCustomerOrders.as_view()),

    # tax list
    # path('tax/', views.TaxListCreate.as_view()),
    # path('tax/<int:pk>/', views.TaxListDetail.as_view()),
    path('userdata/<int:pk>/', views.UserDataDetail.as_view()),
    path('add-to-wishlist/', views.WishlistCreateView.as_view()),
    path('remove-from-wishlist/', views.WishlistDeleteView.as_view()),
    path('my-wishlist/', views.MyWishlistView.as_view()),
]
