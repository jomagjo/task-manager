from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .forms import SignupForm, TaskForm
from .models import Task
from .serializers import TaskSerializer


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = SignupForm()
    return render(request, "tasks/signup.html", {"form": form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
