from django.db import models

# Create your models here.

class UserAcl(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)
    password = models.CharField(max_length=200)

class UserHistory(models.Model):
    name = models.ForeignKey(UserAcl, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    board = models.CharField(max_length=500)
    endtime = models.DateTimeField()