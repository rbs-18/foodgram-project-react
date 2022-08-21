from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from .views import TagViewSet, IngredientViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users.urls')),
]
