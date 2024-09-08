from django.db.models import Q, Count
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter

from ttracker.models import Employee, Task
from ttracker.paginators import TaskListPagination
from ttracker.serializer import (
    EmployeeSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskSerializer,
    EmployeeActiveTasksSerializer
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


class TaskListAPIView(generics.ListAPIView):
    """показывает все созданные задачи сотрудников по 5 страницу"""

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

