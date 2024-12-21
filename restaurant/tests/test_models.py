from django.test import TestCase
from restaurant.models import MenuItem, Booking


class MenuItemModelTest(TestCase):

    def test_create_menu_item(self):
        """Test creating a MenuItem instance with valid data."""
        item = MenuItem.objects.create(
            title="Pasta", price=12.50, featured=True)
        self.assertEqual(item.title, "Pasta")
        self.assertEqual(item.price, 12.50)
        self.assertTrue(item.featured)

    def test_string_representation(self):
        """Test the string representation of a MenuItem instance."""
        item = MenuItem.objects.create(title="Pizza", price=8.99)
        self.assertEqual(str(item), "Pizza : 8.99")

    def test_default_featured_value(self):
        """Test the default value of the 'featured' field."""
        item = MenuItem.objects.create(title="Burger", price=9.99)
        self.assertFalse(item.featured)

    def test_max_title_length(self):
        """Test that a title exceeding max_length raises an error."""
        long_title = "A" * 256  # 1 character longer than the max_length
        with self.assertRaises(Exception):
            MenuItem.objects.create(title=long_title, price=5.99)

    def test_price_precision(self):
        """Test that the price field supports up to 6 digits and 2 decimals."""
        item = MenuItem.objects.create(title="Ice Cream", price=9999.99)
        self.assertEqual(item.price, 9999.99)
        with self.assertRaises(Exception):
            MenuItem.objects.create(
                title="Expensive Item", price=1000000.00)  # Exceeds max_digits


class BookingModelTest(TestCase):

    def test_create_booking(self):
        """Test creating a Booking instance with valid data."""
        booking = Booking.objects.create(
            name="John Doe",
            guest_number=4,
            date="2024-12-31",
            comment="Birthday celebration"
        )
        self.assertEqual(booking.name, "John Doe")
        self.assertEqual(booking.guest_number, 4)
        self.assertEqual(str(booking.date), "2024-12-31")
        self.assertEqual(booking.comment, "Birthday celebration")

    def test_string_representation(self):
        """Test the string representation of a Booking instance."""
        booking = Booking.objects.create(name="Jane Smith", date="2024-01-01")
        self.assertEqual(str(booking), "Jane Smith : 2024-01-01")

    def test_default_guest_number(self):
        """Test the default value for 'guest_number'."""
        booking = Booking.objects.create(name="Alice", date="2024-10-10")
        self.assertEqual(booking.guest_number, 1)

    def test_null_name(self):
        """Test that 'name' can be null."""
        booking = Booking.objects.create(guest_number=2, date="2024-11-25")
        self.assertIsNone(booking.name)

    def test_max_comment_length(self):
        """Test that 'comment' cannot exceed 1000 characters."""
        long_comment = "A" * 1001  # 1 character longer than the max_length
        with self.assertRaises(Exception):
            Booking.objects.create(
                name="Bob", date="2024-09-15", comment=long_comment)

    def test_null_date(self):
        """Test that 'date' can be null."""
        booking = Booking.objects.create(name="Charlie", guest_number=3)
        self.assertIsNone(booking.date)
