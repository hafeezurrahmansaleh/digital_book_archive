from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(CustomerProfile)
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    def created_at_formated(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    created_at_formated.short_description = 'Joining Date'

    list_display = ('full_name', 'email', 'phone', 'dob', 'city', 'created_at_formated', 'is_active')
    search_fields = ['full_name', 'email', 'phone', 'dob__startswith', 'created_at__startswith', 'is_active']


# admin.site.register(PublisherProfile)
@admin.register(PublisherProfile)
class PublisherProfileAdmin(admin.ModelAdmin):
    def created_at_formated(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    created_at_formated.short_description = 'Joining Date'

    list_display = ('name', 'email', 'created_at_formated', 'is_active')
    search_fields = ['name', 'email', 'created_at__startswith', 'is_active']


admin.site.register(AdminProfile)
# admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('name', 'email')
    search_fields = ['name', 'email']

admin.site.register(Wishlist)
admin.site.register(WishlistItems)