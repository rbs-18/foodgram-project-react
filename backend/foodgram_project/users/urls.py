from django.urls import include, path

from .views import CustomTokenCreateView

app_name = 'users'

urlpatterns = [
    path(
        'auth/token/login/',
        CustomTokenCreateView.as_view(),
        name='custom_login'
    ),
    path('', include('djoser.urls.authtoken')),
]
