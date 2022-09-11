from django.urls import include, path

from .views import TokenCreateByEmailView

app_name = 'users'

urlpatterns = [
    path(
        'auth/token/login/',
        TokenCreateByEmailView.as_view(),
        name='custom_login',
    ),
    path('', include('djoser.urls.authtoken')),
]
