from django.db import models
from django.contrib.auth.models import User

from hashlib import sha224


# Manager's
class TasksMenuManager(models.Manager):
    """
    A Manager to display in the general list
    """

    def single_cat(self, cat):
        return super().get_queryset().filter(cat_id=cat).defer("first_test", "second_test", "third_test", "patterns_id",
                                                               "id", "desc")


# Models
class Type(models.Model):
    catTask = models.CharField(max_length=30, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.catTask


class Task(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя задачки', unique=True)
    desc = models.TextField(max_length=1000)
    cat = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, default=0, null=False)
    hash_name = models.SlugField(editable=False, null=False)
    patterns = models.ForeignKey("ExamplesForTask", on_delete=models.CASCADE)
    first_test = models.TextField(blank=False, null=False)
    second_test = models.TextField(blank=False, null=False)
    third_test = models.TextField(blank=False, null=False)
    cost = models.IntegerField(default=0)
    users_solved = models.ManyToManyField(to=User, db_table="SolvingTasksByUser")
    level = models.CharField(
        max_length=1,
        choices=[
            ('H', 'Hard'),
            ('M', 'Medium'),
            ('E', 'Easy'),
        ],
        default='E'
    )

    class Meta:
        db_table = "Tasks"

    objects = models.Manager()
    tasks_menu = TasksMenuManager()

    def save(self, *args, **kwargs):
        self.hash_name = sha224(self.name.encode()).hexdigest()[:9]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Tasks"


class ExamplesForTask(models.Model):
    python = models.TextField()
    cpp = models.TextField()
    go = models.TextField()

    class Meta:
        db_table = "ExamplesForTasks"

    def __str__(self):
        return "Patterns"
