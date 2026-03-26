from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from project.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker123",
            position=Position.objects.create(name="QA"),
        )

    def test_worker_position_listed(self):
        """
        Test that worker's position listed on worker admin page
        :return:
        """
        url = reverse("admin:project_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_detail_position_listed(self):
        """
        Test that worker's position is on worker detail admin page
        :return:
        """
        url = reverse("admin:project_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_add_fieldsets(self):
        """
        Test that additional fields (first_name, last_name, position)
        are present on worker add admin page
        :return:
        """
        url = reverse("admin:project_worker_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")  # поле присутнє в формі
        self.assertContains(response, "last_name")
        self.assertContains(response, "position")

    def test_task_listed(self):
        url = reverse("admin:project_task_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_position_listed(self):
        url = reverse("admin:project_position_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
