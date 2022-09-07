from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from .views import (
    RecipeViewSet, TagViewSet, IngredientViewSet, SubscribeView
)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('auth/', include('users.urls', namespace='users')),
    path('', include(router.urls)),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
]
