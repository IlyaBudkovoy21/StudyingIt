from django.contrib import admin
from .models import Types, Tasks

admin.site.register(Tasks)
admin.site.register(Types)