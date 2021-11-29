# from audiofield.admin import AudioFileAdmin
from django.contrib import admin
from django.db import models
from .models import *
from user_profile.models import *
# Register your models here.

admin.site.register(ContentType)
# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'type', 'is_active')

admin.site.register(SliderImage)


@admin.register(BookDetails)
class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'short_name', 'isbn', 'author', 'publisher')
    search_fields = ['book_name', 'short_name', 'isbn', 'author__name', 'publisher__name']


admin.site.register(BookContentA)
admin.site.register(BookContentB)
admin.site.register(BookContentC)
admin.site.register(BookContentD)
admin.site.register(BookContentE)
admin.site.register(BookContentF)
admin.site.register(BookContentG)
admin.site.register(BookContentS)
admin.site.register(AudioBook)
# admin.site.register(Review)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'customer', 'subject', 'rating')
    # search_fields = ['book_name', 'short_name', 'isbn', 'author__name', 'publisher__name']


# add 'audio_file_player' tag to your admin view
list_display = (..., 'audio_file_player', ...)
actions = ['custom_delete_selected']
#
# def custom_delete_selected(self, request, queryset):
#     #custom delete code
#     n = queryset.count()
#     for i in queryset:
#         if i.audio_file:
#             if os.path.exists(i.audio_file.path):
#                 os.remove(i.audio_file.path)
#         i.delete()
#     self.message_user(request, ("Successfully deleted %d audio files.") % n)
# custom_delete_selected.short_description = "Delete selected items"
#
# def get_actions(self, request):
#     actions = super(AudioFileAdmin, self).get_actions(request)
#     del actions['delete_selected']
#     return actions



