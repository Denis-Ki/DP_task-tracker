from django.urls import path, include

from rest_framework.routers import SimpleRouter

from ttracker.apps import TtrackerConfig
from ttracker.views import EmployeeAPIView, EmployeeActiveTasksListAPIView

app_name = TtrackerConfig.name

router = SimpleRouter()
router.register(r"employee", EmployeeAPIView, basename="employee")

urlpatterns = [
    path("active_tasks/", EmployeeActiveTasksListAPIView.as_view(), name="employee_active_tasks_list"),
]

urlpatterns += router.urls


