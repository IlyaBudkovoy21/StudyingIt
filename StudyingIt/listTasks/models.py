from django.db import models


class Types(models.Model):
    typeTask = models.CharField(max_length=30)


class Tasks(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=1000)
    type_id = models.ForeignKey(Types, on_delete=models.PROTECT)
