from rest_framework.pagination import PageNumberPagination


class TaskListPagination(PageNumberPagination):
    page_size = 5
