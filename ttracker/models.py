from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Employee(models.Model):
    POSITION_CAT1 = 'category 1'
    POSITION_CAT2 = 'category 2'
    POSITION_CAT3 = 'category 3'
    MANAGER = 'manager'
    POSITIONS = [
        (POSITION_CAT1, 'Инженер 1 категории'),
        (POSITION_CAT2, 'Инженер 2 категории'),
        (POSITION_CAT3, 'Инженер 3 категории'),
        (MANAGER, 'Начальник отдела'),
    ]
    name = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        help_text='введите ФИО'
    )
    position = models.CharField(
        max_length=50,
        choices=POSITIONS,
        default=POSITION_CAT3,
        verbose_name="Должность",
        help_text='выберите должность'
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        help_text='введите служебный email сотрудника'
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон',
        **NULLABLE,
        help_text='введите номер телефона'
    )
    vacation_status = models.BooleanField(
        default=False,
        verbose_name='Статус отпуска',
        help_text='статус нахождения в отпуске'
    )

    def __str__(self):
        return f'{self.name}, {self.position}, {self.email}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Task(models.Model):
    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUSES = [
        (STATUS_OPEN, 'Открыта'),
        (STATUS_IN_PROGRESS, 'В исполении'),
        (STATUS_DONE, 'Закрыта'),
    ]

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
        default=STATUS_OPEN,
        verbose_name="Статус",
        help_text='выберите статус задачи'
    )
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        on_delete=models.CASCADE,
        verbose_name="Создатель",
    )

    def __str__(self):
        return f'{self.title}: {self.status}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


