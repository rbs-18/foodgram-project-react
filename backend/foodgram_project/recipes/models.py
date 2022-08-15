from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tags(models.Model):
    """ Model for tags. """

    name = models.CharField('Name of tag', max_length=200, unique=True)
    color = ColorField('Color', format='hexa')
    slug = models.CharField('Unique slug', max_length=200, unique=True)


class Ingredients(models.Model):
    """ Model for ingredients. """

    name = models.CharField('Name of product', max_length=200, db_index=True)
    measurement_unit = models.CharField('Units', max_length=200)


class Subscriptions(models.Model):
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
    # TODO сделать метод UniqueTogether
