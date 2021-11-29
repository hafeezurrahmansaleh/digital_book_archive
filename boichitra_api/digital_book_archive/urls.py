"""digital_book_archive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.documentation import include_docs_urls

admin.site.site_header = "Boichtra Admin"
admin.site.site_title = "Boichtra Admin Portal"
admin.site.index_title = "Welcome to Boichtra Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('user_auth.urls')),
    path('api/v1/profile/', include('user_profile.urls')),
    path('api/v1/archive/', include('archive.urls')),
    path('api/v1/subscription/', include('subscription.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    url(r'^api/v1/docs/', include_docs_urls(title='Digital Archive API', description=''))
]


urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
