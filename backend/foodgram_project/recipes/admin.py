from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'author',
    )
