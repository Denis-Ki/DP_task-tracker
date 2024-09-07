from datetime import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}

DEPARTMENTS = [
    ('Отдел электроники', 'Отдел электроники'),
    ('Отдел программирования', 'Отдел программирования'),
    ('Конструкторский отдел ', 'Конструкторский отдел'),
    ('Математический отдел ', 'Математический отдел'),
]

POSITIONS = [
    ('Инженер 1 категории', 'Инженер 1 категории'),
    ('Инженер 2 категории', 'Инженер 2 категории'),
    ('Инженер 3 категории', 'Инженер 3 категории'),
    ('Начальник отдела', 'Начальник отдела'),
]

STATUSES = [
    ('Открыта', 'Открыта'),
    ('В исполении', 'В исполении'),
    ('Закрыта', 'Закрыта'),
]


# class Department(models.Model):
#     title = models.CharField(
#         max_length=50,
#         choices=DEPARTMENTS,
#         verbose_name="Отдел",
#         help_text='выберите отдел'
#     )
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Отдел'
#         verbose_name_plural = 'Отделы'


class Employee(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        help_text='введите ФИО'
    )
    position = models.CharField(
        max_length=50,
        choices=POSITIONS,
        verbose_name="Должность",
        help_text='выберите должность'
    )
    # department = models.ForeignKey(
    #     Department,
    #     on_delete=models.CASCADE,
    #     verbose_name="Отдел",
    #     help_text='выберите отдел'
    # )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        help_text='введите служебный email сотрудника'
    )
    phone_number = PhoneNumberField(
        verbose_name="Телефон",
        **NULLABLE,
        help_text='введите номер телефона'
    )

    def __str__(self):
        return f'{self.name}, {self.department}, {self.position}, {self.email}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Task(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name='Название задачи',
        help_text='введите название задачи'
    )
    description = models.TextField(
        verbose_name='Описание',
        **NULLABLE,
        help_text='опишите задачу'
    )
    deadline = models.DateField(
        verbose_name='Срок выполнения',
        help_text='введите срок выполнения'
    )
    parental_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Ссылка на родительскую задачу",
        help_text="Пример: Разработка схемы интерфейса передачи данных может быть связана с разработкой "
                  "схемы вычислителя, как дочерняя задача"
    )
    executor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='Исполнитель',
        help_text='выберите исполнителя'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUSES,
        default='Открыта',
        verbose_name="Статус",
        help_text='выберите статус задачи'
    )
    # department = models.ForeignKey(
    #     Department,
    #     on_delete=models.CASCADE,
    #     verbose_name="Отдел",
    #     help_text='выберите отдел'
    # )

    def is_overdue(self):
        """просроченые задачи"""
        return self.deadline < datetime.date.today()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


