from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ttracker.apps import TtrackerConfig
from ttracker.views import (
    EmployeeAPIView,
    EmployeeActiveTasksListAPIView,
    TaskCreateAPIView,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDestroyAPIView,
    ImportantTasksAPIView,
)
app_name = TtrackerConfig.name

router = DefaultRouter()
router.register(r'employees', EmployeeAPIView, basename='employee')

urlpatterns = [
    path('', include(router.urls)),  # Включаем все URL для CRUD операций с сотрудниками
    path('employees/active-tasks/', EmployeeActiveTasksListAPIView.as_view(), name='employee-active-tasks'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskRetrieveAPIView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateAPIView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDestroyAPIView.as_view(), name='task-delete'),
    path('tasks/important/', ImportantTasksAPIView.as_view(), name='important-tasks'),
]

