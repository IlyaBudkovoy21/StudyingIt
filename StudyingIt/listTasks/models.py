from django.db import models
from django.db.models import F
from hashlib import sha224


class Types(models.Model):
    catTask = models.CharField(max_length=30, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.catTask


class Tasks(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя задачки')
    desc = models.TextField(max_length=1000)
    cat = models.ForeignKey(Types, on_delete=models.CASCADE, blank=False, default=0, null=False)
    hash_name = models.SlugField(editable=False, null=False)

    def __str__(self):
        return self.name
