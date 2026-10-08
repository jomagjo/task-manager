from django.contrib import admin

from .models import Task, TaskList


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "custom_category_label", "created_at")
    list_filter = ("category", "user")
    search_fields = ("name", "custom_category_label")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_list", "due_date", "status", "created_at")
    list_filter = ("status", "task_list")
    search_fields = ("title", "description")
