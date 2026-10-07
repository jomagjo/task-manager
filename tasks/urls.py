from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.task_add, name="task_add"),
    path("api/tasks/", views.TaskListCreateAPIView.as_view(), name="task_api_list_create"),
]
