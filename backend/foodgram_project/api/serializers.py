from rest_framework import serializers

from recipes.models import Ingredient, Subscription, Tag


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


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer for Subcription model. """

    class Meta:
        model = Subscription
        # fields = ()
