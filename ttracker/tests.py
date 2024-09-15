
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ttracker.models import Task, Employee
from users.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@mail.ru",
            password="testpas"
        )

        self.employee = Employee.objects.create(
            name="Тестов Тест Тестович",
            position='category 1',
            email="testemployee@mail.ru",
            vacation_status=False
        )
        self.task = Task.objects.create(
            title="TestTask1",
            deadline="2024-09-21",
            status="in_progress",
            executor=Employee.objects.get(pk=self.employee.id),
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        """"Тестирование просмотра задачи"""
        url = reverse("ttracker:task-detail", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.task.title)

    def test_task_create(self):
        """Тестирование создания задачи"""
        url = reverse("ttracker:task-create")
        data = {
            "title": "TestTask2",
            "deadline": "2024-09-22",
            "executor": self.employee.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_update(self):
        """Тестирование обновления задачи"""
        url = reverse("ttracker:task-update", args=(self.task.pk,))
        data = {"title": "NewTestTask"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "NewTestTask")

    def test_task_destroy(self):
        """Тестирование удаления задачи"""
        url = reverse("ttracker:task-delete", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_task_list(self):
        """Тестирование просмотра списка задач"""
        url = reverse("ttracker:task-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": self.task.pk,
                    "title": "TestTask1",
                    "description": None,
                    "deadline": "2024-09-21",
                    "parental_task": None,
                    "executor": self.task.executor.id,
                    "status": "in_progress",
                    "owner": None,
                }
                ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class EmployeeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@mail.ru",
            password="adminpass"
        )
        self.employee = Employee.objects.create(
            name="Иванов Иван Иванович",
            position=Employee.POSITION_CAT1,
            email="ivanov@mail.ru",
            vacation_status=False
        )
        self.client.force_authenticate(user=self.user)

    def test_employee_retrieve(self):
        """Тестирование получения информации о сотруднике"""
        url = reverse("ttracker:employee-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], self.employee.name)
        self.assertEqual(data["email"], self.employee.email)

    def test_employee_create(self):
        """Тестирование создания нового сотрудника"""
        url = reverse("ttracker:employee-list")
        data = {
            "name": "Петров Петр Петрович",
            "position": Employee.POSITION_CAT2,
            "email": "petrov@mail.ru",
            "vacation_status": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(email="petrov@mail.ru").name, "Петров Петр Петрович")

    def test_employee_update(self):
        """Тестирование обновления информации о сотруднике"""
        url = reverse("ttracker:employee-detail", args=(self.employee.pk,))
        data = {"name": "Иванов Иван"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_employee = Employee.objects.get(pk=self.employee.pk)
        self.assertEqual(updated_employee.name, "Иванов Иван")

    def test_employee_destroy(self):
        """Тестирование удаления сотрудника"""
        url = reverse("ttracker:employee-detail", args=(self.employee.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_employee_list(self):
        """Тестирование просмотра списка сотрудников"""
        url = reverse("ttracker:employee-list")
        response = self.client.get(url)
        data = response.json()
        expected_result = [
                {
                    "id": self.employee.pk,
                    "name": "Иванов Иван Иванович",
                    "position": "category 1",
                    "email": "ivanov@mail.ru",
                    "phone_number": None,
                    "vacation_status": False
                }
            ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)

    def test_employee_active_tasks_list(self):
        """Тестирование списка сотрудников по степени занятости"""
        # Создаем сотрудника с задачами
        employee_with_tasks = Employee.objects.create(
            name="Петров Петр Петрович",
            position=Employee.POSITION_CAT2,
            email="petrov@mail.ru",
            vacation_status=False
        )
        # Создаем задачи для сотрудника
        Task.objects.create(title="Задача 1", executor=employee_with_tasks, status="in_progress", deadline="2024-09-30")
        Task.objects.create(title="Задача 2", executor=employee_with_tasks, status="in_progress", deadline="2024-09-30")

        url = reverse("ttracker:employee-active-tasks")
        response = self.client.get(url)
        data = response.json()

        # Проверяем, что сотрудник с задачами отображается первым
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], "Петров Петр Петрович")
        self.assertEqual(data[0]['count_active_tasks'], 2)


