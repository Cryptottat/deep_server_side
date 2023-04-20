from django.contrib import admin

from .models import ThreadInfo



class AdminThreadInfo(admin.ModelAdmin):
    model = ThreadInfo
    list_display = (
        'host_name',
        'anydesk_id',
        'hai_ip_account',
        'total_logged_in',
        'thread_index',
        'server_num',
        'proxy',
        'google_id',
        'google_password',
        'google_email',
        # 'user_agent',
        'google_logged_in',
        'keyword',
        'is_filter',
        'target_url',
        'enter_type',
        'now_state',
        'target_state',
        'last_connected_timestamp'
    )

admin.site.register(ThreadInfo,AdminThreadInfo)
# Register your models here.
