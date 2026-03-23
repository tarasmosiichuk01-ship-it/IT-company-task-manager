from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from project.forms import (
    SignUpForm,
    TaskSearchForm,
    PositionSearchForm,
    WorkerSearchForm,
    WorkerCreationForm,
    TaskTypeSearchForm,
    TaskForm,
    ProjectForm,
    ProjectSearchForm,
    TeamForm,
    TeamSearchForm,
)
from project.models import Worker, Task, Position, TaskType, Project, Team


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_positions": num_positions,
        "num_visits": num_visits,
    }
    return render(request, "project/index.html", context=context)


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success})

class PositionListView(generic.ListView):
    model = Position
    queryset = Position.objects.all()
    context_object_name = "position_list"
    template_name = "project/position_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("project:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("project:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("project:position-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    queryset = TaskType.objects.all()
    template_name = "project/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("project:task-type-list")
    template_name = "project/task_type_form.html"


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    template_name = "project/task_type_detail.html"


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "project/task_type_confirm_delete.html"
    success_url = reverse_lazy("project:task-type-list")


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "task_list"
    template_name = "project/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("project:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("project:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("project:task-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.all()
    context_object_name = "worker_list"
    template_name = "project/worker_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["username"] = username
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(username__icontains=form.cleaned_data["username"])
        return self.queryset

class WorkerDetailView(generic.DetailView):
    model = Worker


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("project:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("project:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("project:worker-list")


class ProjectListView(generic.ListView):
    model = Project
    queryset = Project.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class ProjectDetailView(generic.DetailView):
    model = Project


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("project:project-list")


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("project:project-list")


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("project:project-list")


class TeamListView(generic.ListView):
    model = Team
    queryset = Team.objects.all()
    paginate_by = 5


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = TeamSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TeamDetailView(generic.DetailView):
    model = Team


class TeamCreateView(generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("project:team-list")


class TeamUpdateView(generic.UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("project:team-list")


class TeamDeleteView(generic.DeleteView):
    model = Team
    success_url = reverse_lazy("project:team-list")


@login_required
def toggle_assign_to_task(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (Task.objects.get(id=pk) in worker.tasks.all()):
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("project:task-detail", args=[pk]))
