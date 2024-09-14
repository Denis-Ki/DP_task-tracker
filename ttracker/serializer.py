from django.db.models import Q
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from ttracker.models import Employee, Task
from ttracker.validators import TitleValidator


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


# class EmployeeActiveTasksSerializer(ModelSerializer):
#     active_tasks_count = SerializerMethodField()
#     tasks = SerializerMethodField()
#
#     def get_active_tasks_count(self, employee):
#         return Task.objects.filter(Q(executor=employee.id), Q(is_active=True)).count()
#
#     def get_tasks(self, employee):
#         tasks = Task.objects.filter(executor=employee.id)
#         tasks_list = []
#         for task in tasks:
#             if task.is_active:
#                 tasks_list.append(task.title)
#         return tasks_list

class EmployeeActiveTasksSerializer(ModelSerializer):
    count_active_tasks = SerializerMethodField()
    tasks = SerializerMethodField()

    def get_count_active_tasks(self, employee):  # Считаем только активные задачи для текущего сотрудника
        return Task.objects.filter(executor=employee.id, is_active=True).count()

    def get_tasks(self, employee): # Фильтруем задачи сразу по активности
        tasks = Task.objects.filter(executor=employee.id, is_active=True).values_list('title', flat=True)
        return list(tasks)

    class Meta:
        model = Employee
        fields = ("name", "tasks", "count_active_tasks")


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            TitleValidator(field="title"),
            UniqueTogetherValidator(fields=["title"], queryset=Task.objects.all()),
        ]


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskListSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class ImportantTaskSerializer(ModelSerializer):
    executor = SerializerMethodField()

    class Meta:
        model = Task
        fields = ['title', 'deadline', 'executor']

    def get_executor(self, task):
        # Получение сотрудников для вывода ФИО
        employees = self.context.get('employees', [])
        return [employee.name for employee in employees]

