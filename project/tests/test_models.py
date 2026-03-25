from django.contrib.auth import get_user_model
from django.test import TestCase

from project.models import Position, TaskType, Worker, Task, Project, Team


class ModelTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), task_type.name)

    def test_worker_str(self):
        worker = Worker.objects.create_user(
            username="john_woody",
            password="test123",
            first_name="John",
            last_name="Woody",
        )
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.get_full_name()})"
        )

    def test_create_worker_with_position(self):
        username = "jack_stone"
        password = "test123"
        position = Position.objects.create(name="QA")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(password))

    def test_task_str(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="test",
            task_type=task_type
        )
        self.assertEqual(str(task), task.name)

    def test_project_str(self):
        project = Project.objects.create(name="test")
        self.assertEqual(str(project), project.name)

    def test_team_str(self):
        team = Team.objects.create(name="test")
        self.assertEqual(str(team), team.name)

    def test_worker_str_without_full_name(self):
        worker = Worker.objects.create_user(username="noname", password="test123")
        self.assertEqual(str(worker), "noname")  # має повертати лише username

    def test_worker_get_absolute_url(self):
        worker = Worker.objects.create_user(username="test", password="test123")
        self.assertEqual(worker.get_absolute_url(), f"/workers/{worker.pk}/")

    def test_task_default_priority(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="test", task_type=task_type)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_default_is_completed(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="test", task_type=task_type)
        self.assertFalse(task.is_completed)