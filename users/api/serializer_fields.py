from rest_framework import serializers
from datetime import timedelta


class LeaveDurationField(serializers.Field):
    def to_representation(self, value):
        return value.days

    def to_internal_value(self, data):
        try:
            days = int(data)
            return timedelta(days=days)
        except ValueError:
            raise serializers.ValidationError('Must be an integer representing days.')