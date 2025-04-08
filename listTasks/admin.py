from django.contrib import admin
from .models import Type, Task, ExamplesForTask


@admin.register(ExamplesForTask)
class CodePatternsAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cat')
    list_display_links = ('id',)
    ordering = ('cat_id',)
    list_editable = ('name', 'cat')
    list_per_page = 20
    search_fields = ['name', 'id']
    list_filter = ['cat', ]


@admin.register(Type)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'catTask')
    list_display_links = ('catTask',)
    ordering = ('id',)
