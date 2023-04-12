from django.db import models

# Create your models here.

class TaskData(models.Model):
    run = models.CharField(max_length=20, null=False, default=False)
    server_num = models.CharField(max_length=20, null=False, default=False)
    keyword = models.CharField(max_length=100, null=False, default=False)
    link = models.CharField(max_length=100, null=False, default=False)
    time_info = models.CharField(max_length=100,null=False, default=False)

    class Meta:
        db_table = 'task_data'
        verbose_name = '작업 정보 테이블'