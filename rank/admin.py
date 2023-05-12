from django.contrib import admin

# Register your models here.
from .models import Announcement,PricePerHour

class AdminAnnouncement(admin.ModelAdmin):
    model = Announcement
    list_display = (
        'subject',
        'create_date',
    )

class AdminPricePerHour(admin.ModelAdmin):
    model = PricePerHour
    # list_display = (
    #     'subject',
    #     'create_date',
    # )
# Register your models here.

# Register your models here.
admin.site.register(Announcement,AdminAnnouncement)
admin.site.register(PricePerHour,AdminPricePerHour)