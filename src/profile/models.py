from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    count_tasks_easy = models.IntegerField(default=0)
    count_tasks_medium = models.IntegerField(default=0)
    count_tasks_hard = models.IntegerField(default=0)


class DatesInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    day_start_row = models.DateField(null=True)
    days_in_row = models.IntegerField(default=0)
    max_days = models.IntegerField(default=0)

    class Meta:
        db_table = "UsersSolutionStreak"
        verbose_name = "Date information"
        verbose_name_plural = "Dates information"
