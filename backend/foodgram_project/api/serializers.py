from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import UserSerializer
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingList, Tag
)


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

    def create_ingredient_recipe_object(self, recipe):
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
        self.create_ingredient_recipe_object(recipe)
        return recipe

    def update(self, instance, validated_data):
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredient_recipe_object(instance)
        instance.tags.set(validated_data.pop('tags'))
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        return instance

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

    def get_is_obj(self, recipe, obj):
        return obj.objects.filter(
            user=self.context.get('request').user.id,
            recipe=recipe,
        ).exists()

    def get_is_favorited(self, obj):
        return self.get_is_obj(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.get_is_obj(obj, ShoppingList)
