from django.db import models

## DataFrame 속성
# id (pk)
# name
# kind
# html
# 


## Plot 속성

# Create your models here.
class Dataframe(models.Model):
    def __str__(self):
        return "%s DataFrame" % self.name
    # id (pk)
    name = models.CharField(max_length=40, null=False, unique=True)
    _html = models.TextField()

class Graph_plot(models.Model):
    def __str__(self):
        return "%s-%s (hue=%s) Plot" % (self.x, self.y, self.hue)

    # id (pk)
    name = models.CharField(max_length=60, null=False, unique=True)
    x = models.CharField(default="", max_length=30)
    y = models.CharField(default="", max_length=30)
    hue = models.CharField(max_length=30, null=True)
    _html = models.TextField()

