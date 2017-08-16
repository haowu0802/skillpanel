from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Tracker(models.Model):

    def get_absolute_url(self):
        return reverse('view_tracker', args=[self.id])


class Log(models.Model):
    text = models.TextField(blank=False)
    tracker = models.ForeignKey(Tracker, default=None)
