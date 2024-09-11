from django.db.models import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter

from ttracker.models import Employee, Task
from ttracker.paginators import TaskListPagination
from ttracker.serializer import (
    EmployeeSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskSerializer,
    EmployeeActiveTasksSerializer,
    ImportantTaskSerializer
)


class EmployeeAPIView(viewsets.ModelViewSet):
    """CRUD сотрудников"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeActiveTasksListAPIView(generics.ListAPIView):
    """Контроллер вывода сотрудников по степени занятости"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveTasksSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name",]

    def get_queryset(self):
        self.queryset = Employee.objects.all()
        self.queryset = self.queryset.select_related()
        self.queryset = Employee.objects.annotate(tasks_count=Count("task")).order_by(
            "-tasks_count"
        )
        return self.queryset


class TaskCreateAPIView(generics.CreateAPIView):
    """создание задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        task.owner = self.request.user
        task.save()


class TaskListAPIView(generics.ListAPIView):
    """показывает все созданные задачи сотрудников по 5 страниц"""

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    pagination_class = TaskListPagination


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """детальный просмотр задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer


class TaskUpdateAPIView(generics.UpdateAPIView):
    """редактирование задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(generics.DestroyAPIView):
    """удаление задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ImportantTasksAPIView(generics.ListAPIView):
    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        # Получаем важные задачи, которые не взяты в работу,
        # но от которых зависят другие задачи
        important_tasks = Task.objects.filter(
            status=Task.STATUS_OPEN,
            is_active=True,
            parental_task__status=Task.STATUS_IN_PROGRESS
        ).order_by('deadline')

        return important_tasks

    def list(self, request, *args, **kwargs):
        # Получаем важные задачи с помощью get_queryset
        important_tasks = self.get_queryset()

        if not important_tasks.exists():
            return Response(
                {"detail": "No important tasks found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Находим сотрудников, которые не в отпуске, и их загруженность
        employees_with_task_count = Employee.objects.filter(
            vacation_status=False  # Проверка, что сотрудник не в отпуске
        ).annotate(task_count=Count('task')).order_by('task_count')

        if not employees_with_task_count.exists():
            return Response(
                {"detail": "No available employees found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Находим наименее загруженного сотрудника
        least_loaded_employee = employees_with_task_count.first()

        task_employee_mapping = []
        employee_index = 0

        for task in important_tasks:
            # Проверка на исполнителя родительской задачи
            parent_task = task.parental_task
            assigned_employee = None

            if parent_task and parent_task.executor:
                # Получаем сотрудника, выполняющего родительскую задачу
                parent_executor = parent_task.executor

                # Проверяем, если у него не более чем на 2 задачи больше, чем у наименее загруженного сотрудника
                if parent_executor.task_set.count() <= least_loaded_employee.task_count + 2:
                    assigned_employee = parent_executor

            # Если родительский сотрудник не подходит, назначаем наименее загруженного сотрудника
            if not assigned_employee:
                if employee_index >= len(employees_with_task_count):
                    employee_index = 0
                assigned_employee = employees_with_task_count[employee_index]
                employee_index += 1

            # Добавляем задачу и сотрудника в список
            task_employee_mapping.append({
                "task": task,
                "employee": assigned_employee
            })

        # Сериализация данных
        serializer = self.get_serializer([task["task"] for task in task_employee_mapping], many=True)
        result = []
        for i, data in enumerate(serializer.data):
            data['executor'] = [task_employee_mapping[i]["employee"].name]
            result.append(data)

        return Response(result, status=status.HTTP_200_OK)
