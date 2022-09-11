from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe,
    ShoppingCart, Subscription, Tag,
)
from users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model. """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for Ingredient model. """

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.Serializer):
    """ Ingredient serializer for create recipe. """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = '__all__'


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ Serializer for create Recipe objects. """

    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipe_set',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def _create_ingredient_recipe_object(self, recipe):
        for ingredient in self.initial_data.get('ingredients'):
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient.get('id'),
            )
            IngredientRecipe.objects.create(
                amount=ingredient.get('amount'),
                recipe=recipe,
                ingredient=current_ingredient,
            )

    def create(self, validated_data):
        validated_data.pop('ingredientrecipe_set')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self._create_ingredient_recipe_object(recipe)

        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('ingredientrecipe_set')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self._create_ingredient_recipe_object(instance)

        instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data
        return data


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for Recipe model. """

    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        queryset = obj.ingredients_list.all()
        return IngredientRecipeSerializer(queryset, many=True).data

    def _get_method_field(self, recipe, obj):
        return obj.objects.filter(
            user=self.context.get('request').user.id,
            recipe=recipe,
        ).exists()

    def get_is_favorited(self, obj):
        return self._get_method_field(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self._get_method_field(obj, ShoppingCart)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """ Serializer for presentation in User serializers. """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer for Subscription model. """

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            follower=obj.follower,
            author=obj.author,
        ).exists()

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author_id)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
