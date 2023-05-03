from django.contrib import admin

# Register your models here.
from .models import User

class AdminUser(admin.ModelAdmin):
    model = User
    list_display = (
        'username',
        'email',
        'point',
    )
# Register your models here.
admin.site.register(User,AdminUser)
