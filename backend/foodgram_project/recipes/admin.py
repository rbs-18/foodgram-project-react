from django.contrib import admin

from .models import Subscriptions

@admin.register(Subscriptions)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'author',
    )
