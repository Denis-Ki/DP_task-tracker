from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        help_text='введите ФИО',
        **NULLABLE,
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email адрес"
    )

    phone = PhoneNumberField(
        verbose_name="телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )

    token = models.CharField(
        max_length=100,
        verbose_name="Token",
        **NULLABLE
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
