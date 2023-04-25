from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('username', 'first_name', 'email')
    list_filter = ('username', 'first_name', 'email')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following', )
    empty_value_display = '-пусто-'
