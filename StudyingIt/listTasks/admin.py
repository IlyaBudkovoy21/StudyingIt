from django.contrib import admin
from .models import Types, Tasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cat', 'hash_name')
    list_display_links = ('id',)
    ordering = ('cat_id',)
    list_editable = ('name', 'cat')
    list_per_page = 20
    search_fields = ['name', 'id']
    list_filter = ['cat', ]


@admin.register(Types)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'catTask')
    list_display_links = ('catTask',)
    ordering = ('id',)
