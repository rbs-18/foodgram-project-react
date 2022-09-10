from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """ Model for tags. """

    name = models.CharField('Name of tag', max_length=200, unique=True)
    color = ColorField('Color')
    slug = models.CharField('Unique slug', max_length=200, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Model for ingredients. """

    name = models.CharField('Name of product', max_length=200, db_index=True)
    measurement_unit = models.CharField('Units', max_length=200)

    def __str__(self):
        return self.name


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_subscription'
            )
        ]


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
    image = models.ImageField('Image', upload_to='recipes/')
    name = models.CharField('Name', max_length=200)
    text = models.TextField('Description')
    cooking_time = models.PositiveIntegerField('Duration of cooking')

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """
    Model for many to many realization between Recepie and Ingridient models.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_list',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.ingredient} for {self.recipe}'


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
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]

    def __str__(self):
        return self.recipe


class ShoppingList(models.Model):
    """ Model for shopping list. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_list',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoping_list',
        verbose_name='Recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            )
        ]

    # def __str__(self):
    #     return self.recipe.
