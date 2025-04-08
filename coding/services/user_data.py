from datetime import datetime, timedelta

from django.contrib.auth.models import User

from profile.models import DatesInfoUser
from listTasks.models import Task


def update_user_streak(info_user: DatesInfoUser):
    if info_user.day_start_row and info_user.day_start_row + timedelta(
            days=info_user.days_in_row) == datetime.now().date():
        info_user.days_in_row += 1
    else:
        info_user.days_in_row = 1
        info_user.day_start_row = datetime.now().date()
    info_user.max_days = max(info_user.max_days, info_user.days_in_row)
    info_user.save()

def update_solution_streak_info(user_id: int, user: User, task: Task) -> None:
    info_user = DatesInfoUser.objects.get_or_create(
        user__id=user_id,
        defaults={'user': user}
    )

    update_user_streak(info_user[0])
    task.users_solved.add(user)
