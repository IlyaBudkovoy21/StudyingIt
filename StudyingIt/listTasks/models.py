from django.db import models
from hashlib import sha224


# Manager's
class TasksMenuManager(models.Manager):
    """
    A Manager to display in the general list
    """
    def single_cat(self, cat):
        return super().get_queryset().filter(cat_id=cat).defer("first_test", "second_test", "third_test", "patterns")


# Models
class Types(models.Model):
    catTask = models.CharField(max_length=30, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.catTask


class Tasks(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя задачки', unique=True)
    desc = models.TextField(max_length=1000)
    cat = models.ForeignKey(Types, on_delete=models.CASCADE, blank=False, default=0, null=False)
    hash_name = models.SlugField(editable=False, null=False)
    patterns = models.ForeignKey("CodePatterns", on_delete=models.CASCADE)
    first_test = models.TextField(blank=False, null=False)
    second_test = models.TextField(blank=False, null=False)
    third_test = models.TextField(blank=False, null=False)
    cost = models.IntegerField(default=0)

    objects = models.Manager()
    tasks_menu = TasksMenuManager()

    def save(self, *args, **kwargs):
        self.hash_name = sha224(self.name.encode()).hexdigest()[:9]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CodePatterns(models.Model):
    python = models.TextField()
    cpp = models.TextField()
    go = models.TextField()

    def __str__(self):
        return "Patterns"
