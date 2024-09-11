from django.contrib import admin

from ttracker.models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "position",
        "vacation_status",
        "email",
        "phone_number",
    )
    list_filter = ("vacation_status",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "executor",
        "parental_task",
        "deadline",
        "status",
        "description",
        "owner",
    )