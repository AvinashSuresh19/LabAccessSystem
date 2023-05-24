from django.db import models

# Create your models here.
class news(models.Model):
    title = models.CharField(max_length=50,default="Tower News")
    description = models.CharField(max_length=255,default="N/A")
    newstype = models.CharField(max_length=15,default="information")
    def __str__(self):
        return self.date_time
		
class userData(models.Model):
    date_time = models.CharField(max_length=30,default="N/A")
    fname = models.CharField(max_length=25,default="N/A")
    lname = models.CharField(max_length=25,default="N/A")
    department = models.CharField(max_length=20,default="N/A")
    entry = models.CharField(max_length=10,default="N/A")
    exit = models.CharField(max_length=10,default="N/A")
    location = models.CharField(max_length=10,default="N/A")
    visitors = models.CharField(max_length=5,default="0")
    personalNo = models.CharField(max_length=10,default="N/A")
    def __str__(self):
        return self.date_time

class userTempData(models.Model):
    date_time = models.CharField(max_length=30,default="N/A")
    fname = models.CharField(max_length=25,default="N/A")
    lname = models.CharField(max_length=25,default="N/A")
    department = models.CharField(max_length=20,default="N/A")
    entry = models.CharField(max_length=10,default="N/A")
    exit = models.CharField(max_length=10,default="N/A")
    personalNo = models.CharField(max_length=10,default="N/A")
    def __str__(self):
        return self.date_time

class ris(models.Model):
    mtype = models.CharField(max_length=20,default="<event>")
    title = models.CharField(max_length=50,default="News")
    description = models.CharField(max_length=255,default="N/A")
    def __str__(self):
        return self.date_time