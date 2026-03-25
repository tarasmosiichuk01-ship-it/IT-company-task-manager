from django.test import TestCase

from project.forms import WorkerCreationForm, TaskForm
from project.models import Position, TaskType


class FormsTests(TestCase):
    def test_worker_creation_form_with_position_first_last_name_is_valid(self):
        position = Position.objects.create(name="Test Position")
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position,
        }
        expected_data = {
            "username": "new_user",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        for field, value in expected_data.items():
            self.assertEqual(form.cleaned_data[field], value)

    def test_task_form_valid(self):
        task_type = TaskType.objects.create(name="Bug")
        form_data = {
            "name": "Test task",
            "priority": "medium",
            "task_type": task_type.id,
            "is_completed": False,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_passwords_mismatch(self):
        form_data = {
            "username": "user",
            "password1": "password123",
            "password2": "different123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_name_search_form_empty_is_valid(self):
        from project.forms import NameSearchForm

        form = NameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
