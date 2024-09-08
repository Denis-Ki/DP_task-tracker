from django.db.models import Q
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from ttracker.models import Employee, Task


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeActiveTasksSerializer(ModelSerializer):
    count_active_tasks = SerializerMethodField()
    tasks = SerializerMethodField()

    def get_count_active_tasks(self, employee):
        return Task.objects.filter(Q(executor=employee.id), Q(is_active=True)).count()

    def get_tasks(self, employee):
        tasks = Task.objects.filter(executor=employee.id)
        tasks_list = []
        for task in tasks:
            if task.is_active:
                tasks_list.append(task.title)
        return tasks_list

    class Meta:
        model = Employee
        fields = ("name", "tasks", "count_active_tasks")


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskListSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
