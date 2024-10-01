from django.db import models


class Types(models.Model):
    catTask = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.catTask


class Tasks(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=1000)
    cat = models.ForeignKey(Types, on_delete=models.CASCADE, blank=False, default=0, null=False)

    def __str__(self):
        return self.name
