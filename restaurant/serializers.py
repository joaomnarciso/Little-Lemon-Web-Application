from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import MenuItem, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class MenuItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured']


class BookingSerializer(serializers.ModelSerializer):
    guest_number = serializers.IntegerField(min_value=1)

    class Meta:
        model = Booking
        fields = ['id', 'name', 'guest_number', 'date', 'comment']

    def validate_date(self, value):
        """Ensure the date is in the future"""
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Booking date cannot be in the past.")
        return value
