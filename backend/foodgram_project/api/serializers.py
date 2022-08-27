from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import UserSerializer
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, Subscription, Tag,
    TagRecipe
)


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model. """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for Ingredient model. """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientForCreateRecipeSerializer(serializers.Serializer):
    """ Ingredient serializer for create recipe. """

    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


# class IngredientForShowRecipeSerializer(serializers.ModelSerializer):
#     """ Ingredient serializer for show recipe. """

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ Serializer for create Recipe objects. """

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientForCreateRecipeSerializer(
        source="ingredientrecipe_set", many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart'
            'name',
            # 'image',
            'text',
            'cooking_time',
        )

    def create_tag_recipe_object(self, recipe, tags):
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag)

    def create_ingredient_recipe_object(self, recipe, ingredients):
        for ingredient_item in ingredients:
            id = ingredient_item.get('id')
            amount = ingredient_item.get('amount')
            ingredient_by_id = get_object_or_404(Ingredient, id=id)

            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_by_id,
                amount=amount,
            )

    def create(self, validated_data):
        print(validated_data)
        # tags = validated_data.pop('tags')
        # ingredients = validated_data.pop('ingredients')
        # recipe = Recipe.objects.create(**validated_data)
        # self.create_tag_recipe_object(recipe, tags)
        # self.create_ingredient_recipe_object(recipe, ingredients)
        # return recipe
        validated_data.pop("ingredientrecipe_set")
        tags = validated_data.pop("tags")
        user = self.context["request"].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in self.initial_data.get("ingredients"):
            current_ingredient = get_object_or_404(Ingredient, id=ingredient["id"])
            IngredientRecipe.objects.create(
                amount=ingredient["amount"],
                recipe=recipe,
                ingredient=current_ingredient,
            )
        return recipe

    def get_is_favorited(self, obj):
        favorites = Favorite.objects.filter(user=self.context['request'].user)
        if obj in favorites:
            return True
        return False


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for Recipe model. """

    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart'
            'name',
            # 'image',
            'text',
            'cooking_time',
        )


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """ Serializer for Subcription model. """

#     folower = Serizlization

#     class Meta:
#         model = Subscription
#         fields = ('follower')
