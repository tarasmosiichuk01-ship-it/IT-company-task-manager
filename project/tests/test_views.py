from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from project.models import Position, TaskType, Task, Project, Team

POSITION_URL = reverse("project:position-list")
TASKTYPE_URL = reverse("project:task-type-list")
TASK_URL = reverse("project:task-list")
WORKER_URL = reverse("project:worker-list")
PROJECT_URL = reverse("project:project-list")
TEAM_URL = reverse("project:team-list")


class PublicTests(TestCase):
    def test_login_required_position(self):
        response = self.client.get(POSITION_URL)
        self.assertRedirects(response, f"/accounts/login/?next={POSITION_URL}")

    def test_login_required_task_type(self):
        response = self.client.get(TASKTYPE_URL)
        self.assertRedirects(response, f"/accounts/login/?next={TASKTYPE_URL}")

    def test_login_required_task(self):
        response = self.client.get(TASK_URL)
        self.assertRedirects(response, f"/accounts/login/?next={TASK_URL}")

    def test_login_required_worker(self):
        response = self.client.get(WORKER_URL)
        self.assertRedirects(response, f"/accounts/login/?next={WORKER_URL}")

    def test_login_required_project(self):
        response = self.client.get(PROJECT_URL)
        self.assertRedirects(response, f"/accounts/login/?next={PROJECT_URL}")

    def test_login_required_team(self):
        response = self.client.get(TEAM_URL)
        self.assertRedirects(response, f"/accounts/login/?next={TEAM_URL}")


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="jack_thorne",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        Position.objects.create(name="Developer")
        Position.objects.create(name="Designer")
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(list(response.context["position_list"]), list(positions))
        self.assertTemplateUsed(response, "project/position_list.html")

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="Fix bug")
        TaskType.objects.create(name="New feature")
        response = self.client.get(TASKTYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(list(response.context["task_type_list"]), list(task_types))
        self.assertTemplateUsed(response, "project/task_type_list.html")

    def test_retrieve_tasks(self):
        Task.objects.create(
            name="Test task one", task_type=TaskType.objects.create(name="Fix bug")
        )
        Task.objects.create(
            name="Test task two", task_type=TaskType.objects.create(name="New feature")
        )
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertTemplateUsed(response, "project/task_list.html")

    def test_create_worker(self):
        position = Position.objects.create(name="Developer")
        form_data = {
            "username": "new_worker",
            "password1": "user11test",
            "password2": "user11test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position.id,
        }
        self.client.post(reverse("project:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position.id, form_data["position"])

    def test_retrieve_projects(self):
        Project.objects.create(name="Test projects one")
        Project.objects.create(name="Test projects two")
        response = self.client.get(PROJECT_URL)
        self.assertEqual(response.status_code, 200)
        projects = Project.objects.all()
        self.assertEqual(list(response.context["project_list"]), list(projects))
        self.assertTemplateUsed(response, "project/project_list.html")

    def test_retrieve_teams(self):
        Team.objects.create(name="Test team one")
        Team.objects.create(name="Test team two")
        response = self.client.get(TEAM_URL)
        self.assertEqual(response.status_code, 200)
        teams = Team.objects.all()
        self.assertEqual(list(response.context["team_list"]), list(teams))
        self.assertTemplateUsed(response, "project/team_list.html")

    def test_toggle_assign_to_task(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="Test", task_type=task_type)

        self.client.post(reverse("project:toggle-task-assign", args=[task.pk]))
        self.assertIn(task, self.user.tasks.all())

        self.client.post(reverse("project:toggle-task-assign", args=[task.pk]))
        self.assertNotIn(task, self.user.tasks.all())

    def test_task_detail_view(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="Test", task_type=task_type)
        response = self.client.get(reverse("project:task-detail", args=[task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_task_delete(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(name="Test", task_type=task_type)
        self.client.post(reverse("project:task-delete", args=[task.pk]))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_position_create(self):
        self.client.post(reverse("project:position-create"), data={"name": "DevOps"})
        self.assertTrue(Position.objects.filter(name="DevOps").exists())


class BaseAuthenticatedTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)


class PositionSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()
        self.position_1 = Position.objects.create(name="Developer")
        self.position_2 = Position.objects.create(name="Designer")

    def test_search_finds_correct_position(self):
        response = self.client.get(
            reverse("project:position-list"),
            data={"name": self.position_1.name},
        )
        self.assertContains(response, self.position_1.name)

    def test_search_excludes_other_positions(self):
        response = self.client.get(
            reverse("project:position-list"), data={"name": self.position_1.name}
        )
        self.assertNotContains(response, self.position_2.name)

    def test_empty_search_returns_all_positions(self):
        response = self.client.get(reverse("project:position-list"))
        self.assertEqual(
            len(response.context["position_list"]), len(Position.objects.all())
        )


class TaskTypeSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()
        self.task_type_1 = TaskType.objects.create(name="Fix bug")
        self.task_type_2 = TaskType.objects.create(name="New feature")

    def test_search_finds_correct_task_types(self):
        response = self.client.get(
            reverse("project:task-type-list"),
            data={"name": self.task_type_1.name},
        )
        self.assertContains(response, self.task_type_1.name)

    def test_search_excludes_other_task_types(self):
        response = self.client.get(
            reverse("project:task-type-list"), data={"name": self.task_type_1.name}
        )
        self.assertNotContains(response, self.task_type_2.name)

    def test_empty_search_returns_all_task_types(self):
        response = self.client.get(reverse("project:task-type-list"))
        self.assertEqual(
            len(response.context["task_type_list"]), len(TaskType.objects.all())
        )


class TaskSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()
        self.task_1 = Task.objects.create(
            name="Test task one", task_type=TaskType.objects.create(name="Fix bug")
        )
        self.task_2 = Task.objects.create(
            name="Test task two", task_type=TaskType.objects.create(name="New feature")
        )

    def test_search_finds_correct_tasks(self):
        response = self.client.get(
            reverse("project:task-list"),
            data={"name": self.task_1.name},
        )
        self.assertContains(response, self.task_1.name)

    def test_search_excludes_other_tasks(self):
        response = self.client.get(
            reverse("project:task-list"), data={"name": self.task_1.name}
        )
        self.assertNotContains(response, self.task_2.name)

    def test_empty_search_returns_all_tasks(self):
        response = self.client.get(reverse("project:task-list"))
        self.assertEqual(len(response.context["task_list"]), len(Task.objects.all()))


class WorkerSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()
        self.worker_1 = get_user_model().objects.create_user(
            username="molly_sting",
            password="test123",
            position=Position.objects.create(name="Designer"),
        )
        self.worker_2 = get_user_model().objects.create_user(
            username="bob_yellow",
            password="test123",
            position=Position.objects.create(name="Project manager"),
        )

    def test_search_finds_correct_worker(self):
        response = self.client.get(
            reverse("project:worker-list"), data={"username": self.worker_1.username}
        )
        self.assertContains(response, self.worker_1.username)

    def test_search_excludes_other_workers(self):
        response = self.client.get(
            reverse("project:worker-list"), data={"username": self.worker_1.username}
        )
        self.assertNotContains(response, self.worker_2.username)

    def test_empty_search_returns_all_workers(self):
        response = self.client.get(reverse("project:worker-list"))
        self.assertEqual(
            len(response.context["worker_list"]), len(get_user_model().objects.all())
        )


class ProjectSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()

        self.project_1 = Project.objects.create(name="Test project one")
        self.project_2 = Project.objects.create(name="Test project two")

    def test_search_finds_correct_projects(self):
        response = self.client.get(
            reverse("project:project-list"),
            data={"name": self.project_1.name},
        )
        self.assertContains(response, self.project_1.name)

    def test_search_excludes_other_projects(self):
        response = self.client.get(
            reverse("project:project-list"), data={"name": self.project_1.name}
        )
        self.assertNotContains(response, self.project_2.name)

    def test_empty_search_returns_all_projects(self):
        response = self.client.get(reverse("project:project-list"))
        self.assertEqual(
            len(response.context["project_list"]), len(Project.objects.all())
        )


class TeamSearchTest(BaseAuthenticatedTest):
    def setUp(self):
        super().setUp()
        self.team_1 = Team.objects.create(name="Test team one")
        self.team_2 = Team.objects.create(name="Test team two")

    def test_search_finds_correct_teams(self):
        response = self.client.get(
            reverse("project:team-list"),
            data={"name": self.team_1.name},
        )
        self.assertContains(response, self.team_1.name)

    def test_search_excludes_other_teams(self):
        response = self.client.get(
            reverse("project:team-list"), data={"name": self.team_1.name}
        )
        self.assertNotContains(response, self.team_2.name)

    def test_empty_search_returns_all_teams(self):
        response = self.client.get(reverse("project:team-list"))
        self.assertEqual(len(response.context["team_list"]), len(Team.objects.all()))
