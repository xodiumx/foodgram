from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по тексту постов.
        list_filter: возможность фильтрации по дате.
    """

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'