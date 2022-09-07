from django.contrib import admin

from .models import (
    Ingredient, IngredientRecipe, Recipe,
    Subscription, Tag, TagRecipe
)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientRecipe


class RecipeTagInline(admin.TabularInline):
    model = TagRecipe


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'follower', 'author')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeTagInline)
    list_display = (
        'pk',
        'author',
        'image',
        'name',
        'text',
        'cooking_time'
    )


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     inlines = (FavoriteInline,)
#     list_display = ('user',)
