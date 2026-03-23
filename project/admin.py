from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from project.models import Position, TaskType, Worker, Task, Project, Team, Tag


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
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


admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Tag)