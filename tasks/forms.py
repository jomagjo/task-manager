from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, TaskList


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["name", "category", "custom_category_label"]
        widgets = {
            "custom_category_label": forms.TextInput(
                attrs={"placeholder": "e.g. Fitness, Side Project"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        custom_category_label = cleaned_data.get("custom_category_label")
        if category == TaskList.Category.CUSTOM and not custom_category_label:
            self.add_error(
                "custom_category_label",
                "Required when category is Custom.",
            )
        return cleaned_data


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]
