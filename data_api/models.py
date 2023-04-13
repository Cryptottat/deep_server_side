from django.db import models

# Create your models here.

class ProxyInfo(models.Model):
    account = models.CharField(max_length=20, null=False, default=False)
    proxy = models.CharField(max_length=50, null=False, default=False)
    usable = models.BooleanField(default=True)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(max_length=5, null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    class Meta:
        db_table = 'proxy_data'
        verbose_name = '프록시 테이블'

class GoogleAccountInfo(models.Model):
    id = models.CharField(max_length=100, null=False, default=False)
    password = models.CharField(max_length=100, null=False, default=False)
    email = models.CharField(max_length=100, null=False, default=False)
    usable = models.BooleanField(default=True)
    matched_proxy = models.CharField(max_length=50, null=True, default=False)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    class Meta:
        db_table = 'google_data'
        verbose_name = '구글 계정 테이블'

class TaskData(models.Model):
    run = models.CharField(max_length=20, null=False, default=False)
    server_num = models.CharField(max_length=20, null=False, default=False)
    keyword = models.CharField(max_length=100, null=False, default=False)
    link = models.CharField(max_length=100, null=False, default=False)
    time_info = models.CharField(max_length=100,null=False, default=False)

    class Meta:
        db_table = 'task_data'
        verbose_name = '작업 정보 테이블'