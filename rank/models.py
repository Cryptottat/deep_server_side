from django.db import models


class Announcement(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

class Order(models.Model):
    username = models.CharField(max_length=20)
    target_time = models.DateTimeField()
    keyword = models.CharField(max_length=20)
    target_url = models.CharField(max_length=200)
    charge = models.IntegerField()
    order_time = models.DateTimeField()