#coding-utf-8
from django.db import models

# Create your models here.

class Car(models.Model):
    car_title = models.CharField(max_length=300)
    car_icon = models.CharField(max_length=300)
    car_des = models.TextField()
    car_link = models.CharField(max_length=300)
    car_body = models.TextField()
    car_time = models.DateTimeField(auto_now_add=True)
    car_source = models.CharField(max_length=20)
    car_cate = models.CharField(max_length=20)
    # car_publish_time = models.DateTimeField()

    def __unicode__(self):
        return self.car_title








