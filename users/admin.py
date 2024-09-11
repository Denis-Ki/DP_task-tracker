from django.contrib import admin

from users.models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ['email']
