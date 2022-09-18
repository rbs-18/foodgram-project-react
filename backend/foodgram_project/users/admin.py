from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserWithPersonalFieldsAdmin(UserAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
    )
    exclude = ('user_permissions', 'groups')
    list_filter = ('email', 'username')
    search_fields = ('username__startswith', 'email__startswith')
