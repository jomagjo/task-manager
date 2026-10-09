from rest_framework import serializers

from .models import Task, TaskList


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
            self.fields["task_list"].queryset = TaskList.objects.filter(
                user=request.user
            )


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = [
            "id",
            "name",
            "category",
            "custom_category_label",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        category = attrs.get("category", getattr(self.instance, "category", None))
        custom_category_label = attrs.get(
            "custom_category_label",
            getattr(self.instance, "custom_category_label", ""),
        )
        if category == TaskList.Category.CUSTOM and not custom_category_label:
            raise serializers.ValidationError(
                {"custom_category_label": "Required when category is Custom."}
            )
        return attrs
