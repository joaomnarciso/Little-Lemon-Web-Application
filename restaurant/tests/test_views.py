from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from restaurant.models import MenuItem, Booking
from django.contrib.auth.models import User
from decimal import Decimal
import json


class MenuItemTests(APITestCase):

    def setUp(self):
        # Create a user and generate a token
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(
            username='adminuser', password='adminpassword')

        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Create test MenuItems
        self.menu_item_data = {
            'title': 'Ice Cream',
            'price': Decimal('5.99'),
            'featured': True
        }
        self.menu_item = MenuItem.objects.create(**self.menu_item_data)

        self.menu_items_url = reverse('menuitem-list')
        self.single_menu_item_url = reverse(

            'menuitem-detail', args=[self.menu_item.id])

    def test_create_menu_item_as_authenticated_user(self):
        """Test creating a menu item as an authenticated user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            self.menu_items_url, self.menu_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_item_as_admin(self):
        """Test creating a menu item as an admin"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(
            self.menu_items_url, self.menu_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_menu_item_as_admin(self):
        """Test updating a menu item as an admin"""
        updated_data = {'title': 'Updated Ice Cream', 'price': Decimal('6.99')}
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.put(
            self.single_menu_item_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, 'Updated Ice Cream')

    def test_delete_menu_item_as_admin(self):
        """Test deleting a menu item as an admin"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(self.single_menu_item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuItem.objects.count(), 0)


class BookingTests(APITestCase):

    def setUp(self):
        # Create users, tokens, and bookings
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(
            username='adminuser', password='adminpassword')

        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.booking_data = {
            'name': 'Test User',
            'guest_number': 4,
            'date': '2024-12-25',
            'comment': 'Big Party'
        }
        self.booking = Booking.objects.create(**self.booking_data)

        self.booking_url = reverse('booking-list')
        self.single_booking_url = reverse(
            'booking-detail', args=[self.booking.id])

    def test_create_booking_as_authenticated_user(self):
        """Test creating a booking as an authenticated user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            self.booking_url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_booking_as_anonymous_user(self):
        """Test creating a booking as an anonymous user (should be forbidden)"""
        response = self.client.post(
            self.booking_url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_as_admin(self):
        """Test creating a booking as an admin"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(
            self.booking_url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_booking_as_admin(self):
        """Test deleting a booking as an admin"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(self.single_booking_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
