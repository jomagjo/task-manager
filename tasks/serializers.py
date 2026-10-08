from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "task_list",
            "title",
            "description",
            "due_date",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is not None:
            from .models import TaskList

            self.fields["task_list"].queryset = TaskList.objects.filter(
                user=request.user
            )
