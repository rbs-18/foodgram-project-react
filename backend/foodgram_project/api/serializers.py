from dataclasses import fields
from rest_framework import serializers

from recipes.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer for Subcription model. """

    class Meta:
        model = Subscription
        # fields = ()
