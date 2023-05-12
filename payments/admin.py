from django.contrib import admin

# Register your models here.

from .models import PointValue

class AdminPointValue(admin.ModelAdmin):
    model = PointValue
    # list_display = (
    #     'subject',
    #     'create_date',
    # )
# Register your models here.
admin.site.register(PointValue,AdminPointValue)