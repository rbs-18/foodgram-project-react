from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """ Model for tags. """

    name = models.CharField('Name of tag', max_length=200, unique=True)
    color = ColorField('Color', format='hexa')
    slug = models.CharField('Unique slug', max_length=200, unique=True)


class Ingredient(models.Model):
    """ Model for ingredients. """

    name = models.CharField('Name of product', max_length=200, db_index=True)
    measurement_unit = models.CharField('Units', max_length=200)


class Subscription(models.Model):
    """ Model for subscibtions. """

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Following',
    )


class Recipe(models.Model):
    """ Model for recepies. """

    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        through_fields=('recipe', 'tag'),
        related_name='recipes',
        verbose_name='Tags',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        related_name='recepes',
        verbose_name='Ingredients',
    )
    image = models.BinaryField('Image', editable=True,)
    name = models.CharField('Name', max_length=200)
    text = models.TextField('Description')
    cooking_time = models.PositiveIntegerField('Duration of cooking')


class IngredientRecipe(models.Model):
    """
    Model for many to many realization between Recepie and Ingridient models.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()


class TagRecipe(models.Model):
    """
    Model for many to many realization between Recepie and Tag models.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Favorite(models.Model):
    """ Model for favorite recipes. """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipes = models.ManyToManyField(
        Recipe,
        through='RecipeFavorite',
        through_fields=('favorite', 'recipe'),
        verbose_name='Recipe'
    )


class RecipeFavorite(models.Model):
    """
    Model for many to many realization between Favorites and Recepie models.
    """
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
