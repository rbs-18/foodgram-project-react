from importlib.metadata import requires
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Model for users. """

    email = models.EmailField('E-mail', max_length=254)
    username = models.CharField('Name of user', max_length=150, unique=True)
    first_name = models.CharField('First name of user', max_length=150)
    last_name = models.CharField('Last name of user', max_length=150)
    password = models.CharField('Password', max_length=150)
