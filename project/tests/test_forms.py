from django.test import TestCase

from project.forms import WorkerCreationForm
from project.models import Position


class FormsTests(TestCase):
    def test_worker_creation_form_with_position_first_last_name_is_valid(self):
        position = Position.objects.create(name = "Test Position")
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