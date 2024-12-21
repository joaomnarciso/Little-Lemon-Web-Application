from django.shortcuts import render
from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

# Home view


def home(request):
    return render(request, "index.html")


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        # Only allow non-GET methods for Admins
        if self.request.method not in ['GET']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # If you need to add custom logic when creating a menu item, you can override this
        serializer.save()


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        # Only allow non-GET methods for Admins
        if self.request.method not in ['GET']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        # You can add custom logic for updates here if needed
        serializer.save()

    def perform_destroy(self, instance):
        # Custom logic before deleting a menu item, if needed
        instance.delete()


class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Allows a superuser to see all bookings, while regular users can only see their own bookings.
        """
        if self.request.user.is_superuser:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(name=self.request.user.username)

    def get_permissions(self):
        """Only authenticated users can access the list of bookings."""
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Customize the creation of the booking, ensuring the booking is associated with the authenticated user.
        """
        serializer.save(name=self.request.user.username)


class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        """Only admins can retrieve, update, or delete individual bookings."""
        permission_classes = [IsAuthenticated]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        """
        Handle update logic for a booking. You can also add extra logic here.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle delete logic for a booking.
        """
        instance.delete()
