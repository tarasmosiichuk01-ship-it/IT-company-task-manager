from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from project.models import Position, TaskType, Worker, Task, Project, Team


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    search_fields = ("username", "first_name", "last_name")
    list_filter = ("position", )
    ordering = ("username", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                )
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "priority",
        "task_type",
        "deadline",
        "is_completed"
    ]
    search_fields = ["name", "description"]
    list_filter = ["priority", "task_type", "is_completed"]
    filter_horizontal = ["assignees"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("workers", "projects")
