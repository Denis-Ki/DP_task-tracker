
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
            is_active=True,
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
        print(data)
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
                    "is_active": True,
                }
                ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)



