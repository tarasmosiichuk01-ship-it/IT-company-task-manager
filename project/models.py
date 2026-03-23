from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = "position"
        verbose_name_plural = "positions"

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = "task type"
        verbose_name_plural = "task types"

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.position})"

    def get_absolute_url(self):
        return reverse("project:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True
    )

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    tasks = models.ManyToManyField(Task, related_name="projects")

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=63)
    workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
    )
    projects = models.ManyToManyField(Project, related_name="teams")

    class Meta:
        verbose_name = "team"
        verbose_name_plural = "teams"
