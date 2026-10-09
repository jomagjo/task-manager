from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.tasklist_summary, name="tasklist_summary"),
    path("lists/new/", views.tasklist_create, name="tasklist_create"),
    path("lists/<int:pk>/", views.tasklist_detail, name="tasklist_detail"),
    path("lists/<int:list_pk>/add/", views.task_add, name="task_add"),
    path("lists/<int:list_pk>/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path(
        "lists/<int:list_pk>/<int:pk>/delete/",
        views.task_delete,
        name="task_delete",
    ),
    path(
        "lists/<int:list_pk>/<int:pk>/status/",
        views.task_update_status,
        name="task_update_status",
    ),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tasks/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/tasks/", views.TaskCollectionAPIView.as_view(), name="task_api_list_create"),
    path(
        "api/tasks/<int:pk>/",
        views.TaskDetailAPIView.as_view(),
        name="task_api_detail",
    ),
    path(
        "api/lists/",
        views.TaskListCollectionAPIView.as_view(),
        name="tasklist_api_list_create",
    ),
    path(
        "api/lists/<int:pk>/",
        views.TaskListDetailAPIView.as_view(),
        name="tasklist_api_detail",
    ),
]
