from django.db import models


class Types(models.Model):
    catTask = models.CharField(max_length=30)

    def __str__(self):
        return self.catTask


class Tasks(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=1000)
    cat = models.ManyToManyField(Types)

    def __str__(self):
        return self.name