from django.conf import settings
from pytest import fixture
from django.core.management import call_command
from django.db import connection
from listTasks.models import Tasks, Types, CodePatterns


@fixture
def create_db(scope="session", autouse=True):
    orig_db = settings.DATABASES['default'].copy()
    settings.DATABASES['default'] = settings.DATABASES['test']
    call_command('migrate')
    yield
    settings.DATABASES['default'] = orig_db
    for conn in connection.all():
        conn.close()


@fixture
def fill_objects(scope="session", autouse=True):
    t = Types.objects.create(catTask='Programming')
    pat = CodePatterns(python="asdf",
                       cpp="adsf",
                       go="asdf")
    a = Tasks.objects.create(name="Sum of two objects",
                         desc="Description of sum of two objects",
                         cat=a,
                         patterns=pat,
                         first_test="asdf",
                         second_test="asdf",
                         third_test="asdf",
                         cose=100)