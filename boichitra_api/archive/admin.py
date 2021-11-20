# from audiofield.admin import AudioFileAdmin
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ContentType)
admin.site.register(Category)
admin.site.register(SliderImage)
admin.site.register(BookDetails)
admin.site.register(BookContentA)
admin.site.register(BookContentB)
admin.site.register(BookContentC)
admin.site.register(BookContentD)
admin.site.register(BookContentE)
admin.site.register(BookContentF)
admin.site.register(BookContentG)
admin.site.register(BookContentS)
admin.site.register(AudioBook)
admin.site.register(Review)


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
