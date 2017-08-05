from django.db import models

# Create your models here.


class Tracker(models.Model):
    pass


class Log(models.Model):
    text = models.TextField(default='')
    tracker = models.ForeignKey(Tracker, default=None)
