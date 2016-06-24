from __future__ import unicode_literals
from django.db import models


# Create your models here.
class WebPage(models.Model):

    url = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    indexed = models.BooleanField()


class Indexing(models.Model):

    word = models.CharField(max_length=250)
    frequency = models.IntegerField()
    webpage = models.ForeignKey(WebPage)
