# Generated by Django 5.0.7 on 2024-09-14 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ttracker", "0003_remove_task_is_important"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="is_active",
        ),
    ]
