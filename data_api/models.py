from django.db import models

# Create your models here.

class ThreadInfo(models.Model):
    host_name = models.CharField(max_length=20, null=False)
    anydesk_id = models.CharField(max_length=20, null=False)
    hai_ip_account = models.CharField(max_length=20, null=False)
    total_logged_in = models.IntegerField(null=False, default=0)
    thread_index = models.IntegerField(null=False)
    server_num = models.IntegerField(null=True, default=None)
    proxy = models.CharField(max_length=20, null=True, default=None)
    google_id = models.CharField(max_length=50, null=True, default=None)
    google_password = models.CharField(max_length=50, null=True, default=None)
    google_email = models.CharField(max_length=50, null=True, default=None)
    user_agent = models.CharField(max_length=200, null=True, default=None)
    google_logged_in = models.BooleanField(null=False, default=False)
    keyword = models.CharField(max_length=100, null=True, default=None)
    is_filter = models.BooleanField(null=False, default=False)
    target_url = models.CharField(max_length=200, null=True, default=None)
    enter_type = models.CharField(max_length=20, null=True, default=None)
    now_state = models.CharField(max_length=20, null=True, default=None)
    target_state = models.CharField(max_length=20, null=True, default=None)
    last_connected_timestamp = models.BigIntegerField(null=True, default=None)
    class Meta:
        db_table = 'thread_data'
        verbose_name = '스레드 테이블'


class ProxyInfo(models.Model):
    account = models.CharField(max_length=20, null=False, default=False)
    proxy = models.CharField(max_length=50, null=False, default=False)
    usable = models.BooleanField(default=True)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    class Meta:
        db_table = 'proxy_data'
        verbose_name = '프록시 테이블'

class GoogleAccountInfo(models.Model):
    google_id = models.CharField(max_length=100, null=False, default=False)
    google_password = models.CharField(max_length=100, null=False, default=False)
    email = models.CharField(max_length=100, null=False, default=False)
    usable = models.BooleanField(default=True)
    matched_hai_ip_account = models.CharField(max_length=50, null=True, default=None)
    matched_proxy = models.CharField(max_length=50, null=True, default=None)
    user_agent = models.CharField(max_length=150, null=True, default=None)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    class Meta:
        db_table = 'google_data'
        verbose_name = '구글 계정 테이블'

class TaskData(models.Model):
    task_run = models.CharField(max_length=20, null=False, default=False)
    server_num = models.CharField(max_length=20, null=False, default=False)
    keyword = models.CharField(max_length=100, null=False, default=False)
    link = models.CharField(max_length=100, null=False, default=False)
    login_check = models.CharField(max_length=100, null=True, default=None)
    time_info = models.CharField(max_length=100,null=False, default=False)
    get_proxy_make_unusable = models.BooleanField(default=True)
    get_google_account_make_unusable = models.BooleanField(default=True)

    class Meta:
        db_table = 'task_data'
        verbose_name = '작업 정보 테이블'

