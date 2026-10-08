from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.task_add, name="task_add"),
    path("<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tasks/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/tasks/", views.TaskListCreateAPIView.as_view(), name="task_api_list_create"),
    path(
        "api/tasks/<int:pk>/",
        views.TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task_api_detail",
    ),
]
