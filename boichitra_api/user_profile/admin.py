from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(PublisherProfile)
admin.site.register(AdminProfile)
admin.site.register(Author)
admin.site.register(Wishlist)
admin.site.register(WishlistItems)