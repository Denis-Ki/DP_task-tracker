import random
import json
from jinja2 import Template
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fixture_template = """
        [
            {% for i in range(10) %}
            {
                "model": "ttracker.employee",
                "pk": {{ i + 1 }},
                "fields": {
                    "name": "{{ random_choice(['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов', 'Попов', 'Александров', 'Фёдоров', 'Морозов', 'Соколов']) }} {{ random_choice(['Алексей', 'Иван', 'Петр', 'Дмитрий', 'Александр', 'Сергей', 'Олег', 'Максим']) }} {{ random_choice(['Алексеевич', 'Иванович', 'Петрович', 'Сергеевич', 'Александрович', 'Олегович', 'Максимович']) }}",
                    "position": "{{ 'category 1' if i < 3 else ('category 2' if i < 6 else 'category 3') }}",
                    "email": "user{{ i+1 }}@mail.ru",
                    "phone_number": "+79{{ random_digits(9) }}",
                    "vacation_status": {{ random_choice([true, false])|lower }}
                }
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        ]
        """

    # Функции для генерации случайных данных
        def random_choice(choices):
            return random.choice(choices)

        def random_digits(n):
            return ''.join(str(random.randint(0, 9)) for _ in range(n))

        # Подготовка данных для шаблона
        context = {
            'random_choice': random_choice,
            'random_digits': random_digits,
        }

        # Создание шаблона Jinja
        template = Template(fixture_template)

        # Генерация контента
        generated_fixture = template.render(context)

        # Запись результата в JSON файл
        with open('employees_fixture.json', 'w') as f:
            f.write(generated_fixture)

        print("Fixture successfully generated: employees_fixture.json")