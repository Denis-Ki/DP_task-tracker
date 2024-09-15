from django.db.models import Count, Q
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
        """Получает важные задачи, которые не взяты в работу,
        но от которых зависят другие задачи"""
        return Task.objects.filter(
            status=Task.STATUS_OPEN,
            parental_task__status=Task.STATUS_IN_PROGRESS
        ).select_related('parental_task').order_by('deadline')

    def list(self, request, *args, **kwargs):
        """Получает список важных задач и исполнителей """
        important_tasks = self.get_queryset()

        if not important_tasks.exists():
            return Response(
                {"detail": "No important tasks found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем сотрудников, не находящихся в отпуске, с подсчетом их активных задач
        employees_with_task_count = Employee.objects.filter(
            vacation_status=False
        ).annotate(
            task_count=Count('task', filter=Q(task__status=Task.STATUS_IN_PROGRESS))
        ).order_by('task_count')

        if not employees_with_task_count.exists():
            return Response(
                {"detail": "No available employees found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Преобразуем список сотрудников в итератор для циклического распределения
        employees_list = list(employees_with_task_count)
        least_loaded_employee = employees_list[0]
        employee_index = 0  # Начальный индекс для распределения задач

        task_employee_mapping = []

        for task in important_tasks:
            parent_task = task.parental_task
            assigned_employee = None

            if parent_task and parent_task.executor:
                parent_executor = parent_task.executor

                # Проверяем загруженность исполнителя родительской задачи
                if parent_executor.task_set.filter(status=Task.STATUS_IN_PROGRESS).count() <= least_loaded_employee.task_count + 2:
                    assigned_employee = parent_executor

            # Если родительский сотрудник не подходит, назначаем наименее загруженного
            if not assigned_employee:
                if employee_index >= len(employees_list):
                    employee_index = 0  # Перезапускаем индекс, если все сотрудники использованы
                assigned_employee = employees_list[employee_index]
                employee_index += 1

            # Добавляем задачу и сотрудника в список
            task_employee_mapping.append({
                "task": task,
                "employee": assigned_employee
            })

        # Сериализация данных с передачей выбранного исполнителя для каждой задачи через контекст
        serializer = self.get_serializer(
            [task["task"] for task in task_employee_mapping],
            many=True,
            context={'employees': [task["employee"] for task in task_employee_mapping]}
        )

        # Формируем финальный результат с назначенным исполнителем
        result = []
        for i, data in enumerate(serializer.data):
            data['executor'] = task_employee_mapping[i]["employee"].name
            result.append(data)

        return Response(result, status=status.HTTP_200_OK)




