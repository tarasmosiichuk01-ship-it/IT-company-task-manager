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
        worker = Worker.objects.create(
            username="john_woody",
            password="test123",
            first_name="John",
            last_name="Woody",
        )
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.first_name} {worker.last_name})"
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
