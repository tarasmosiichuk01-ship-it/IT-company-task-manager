from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from project.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker123",
            position=Position.objects.create(name="QA")
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
