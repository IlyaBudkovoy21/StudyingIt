from django.core.exceptions import ObjectDoesNotExist

from listTasks.models import Task


def get_task(task_id: int):
    try:
        return Task.objects.only("id", "name").get(id=task_id)
    except ObjectDoesNotExist:
        return None
    except ValueError:
        return None

def get_task_by_hash(hash_name: str):
    try:
        return Task.objects.get(hash_name=hash_name)
    except ObjectDoesNotExist:
        return None
    except ValueError:
        return None

def get_all_tasks():
    return Task.objects.all()
