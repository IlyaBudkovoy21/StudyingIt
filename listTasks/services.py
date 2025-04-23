import json

from django.db.models import Q

from listTasks.models import Task, Type


def return_task_by_one_cat(cat: str):
    return Task.tasks_menu.single_cat(cat)

def return_tasks_menu():
    return Task.tasks_menu.all()

def return_many_cats(categories):
    if not categories:
        return Task.tasks_menu.all()

    query = Q()
    filter_param = json.loads(categories)
    for cat in filter_param:
        query |= Q(cat_id=cat)
    return Task.tasks_menu.filter(query)

def return_all_types():
    return Type.objects.all()

def return_all_tasks():
    return Task.objects.all()
