from django.urls import path
from archive import views

urlpatterns = [
    path('book-content/<int:book_id>/<int:wpp>/', views.BookContent.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('logged-publisher-books/', views.MyBookList.as_view()),
    path('book/<str:short_name>/', views.BookInfo.as_view()),
    path('audio-book/<int:book_id>/', views.AudioBookDetailsView.as_view()),
    path('submit-review/', views.BookReviewListView.as_view()),
    path('get-reviews/', views.BookReviewListView.as_view()),
    path('category/', views.CategoryList.as_view()),
    path('book-request-list/', views.BookRequestListView.as_view()),
    path('create-book-request/', views.BookRequestCreateView.as_view()),
    path('my-book-requests/', views.MyBookRequestListView.as_view()),
    path('category/', views.CategoryList.as_view()),
    path('publisher-books/', views.PublisherBooks.as_view()),
    path('dashboard-content/', views.DashboardContent.as_view()),
    path('search-book/', views.SearchBook.as_view()),
    path('<int:id>/', views.BookDetail.as_view()),
    path('slider-image-list/', views.SliderImageListView.as_view()),
    path('', views.BookList.as_view()),
]
