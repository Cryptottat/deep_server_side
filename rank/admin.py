from django.contrib import admin

# Register your models here.
from .models import Announcement

class AdminAnnouncement(admin.ModelAdmin):
    model = Announcement
    list_display = (
        'subject',
        'create_date',
    )
# Register your models here.
admin.site.register(Announcement,AdminAnnouncement)