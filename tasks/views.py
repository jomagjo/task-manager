from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .forms import SignupForm, TaskForm, TaskListForm
from .models import Task, TaskList
from .serializers import TaskListSerializer, TaskSerializer


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tasklist_summary")
    else:
        form = SignupForm()
    return render(request, "tasks/signup.html", {"form": form})


@login_required
def tasklist_summary(request):
    task_lists = TaskList.objects.filter(user=request.user).annotate(
        total_count=Count("tasks"),
        done_count=Count(
            "tasks", filter=Q(tasks__status=Task.Status.COMPLETED)
        ),
    )
    return render(
        request, "tasks/tasklist_summary.html", {"task_lists": task_lists}
    )


@login_required
def tasklist_create(request):
    if request.method == "POST":
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            return redirect("tasklist_detail", pk=task_list.pk)
    else:
        form = TaskListForm()
    return render(request, "tasks/tasklist_form.html", {"form": form})


@login_required
def tasklist_detail(request, pk):
    task_list = get_object_or_404(TaskList, pk=pk, user=request.user)
    tasks = task_list.tasks.all()
    return render(
        request,
        "tasks/tasklist_detail.html",
        {"task_list_obj": task_list, "tasks": tasks},
    )


@login_required
def task_add(request, list_pk):
    task_list = get_object_or_404(TaskList, pk=list_pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_list = task_list
            task.save()
            return redirect("tasklist_detail", pk=task_list.pk)
    else:
        form = TaskForm()
    return render(
        request, "tasks/task_form.html", {"form": form, "task_list_obj": task_list}
    )


@login_required
def task_edit(request, list_pk, pk):
    task = get_object_or_404(
        Task, pk=pk, task_list_id=list_pk, task_list__user=request.user
    )
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasklist_detail", pk=list_pk)
    else:
        form = TaskForm(instance=task)
    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "task": task, "task_list_obj": task.task_list},
    )


@login_required
@require_POST
def task_update_status(request, list_pk, pk):
    task = get_object_or_404(
        Task, pk=pk, task_list_id=list_pk, task_list__user=request.user
    )
    status = request.POST.get("status")
    if status in Task.Status.values:
        task.status = status
        task.save(update_fields=["status"])
    return redirect("tasklist_detail", pk=list_pk)


@login_required
def task_delete(request, list_pk, pk):
    task = get_object_or_404(
        Task, pk=pk, task_list_id=list_pk, task_list__user=request.user
    )
    if request.method == "POST":
        task.delete()
        return redirect("tasklist_detail", pk=list_pk)
    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task": task, "task_list_obj": task.task_list},
    )


class TaskCollectionAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(task_list__user=self.request.user)
        task_list_id = self.request.query_params.get("task_list")
        if task_list_id:
            queryset = queryset.filter(task_list_id=task_list_id)
        return queryset


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(task_list__user=self.request.user)


class TaskListCollectionAPIView(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)
