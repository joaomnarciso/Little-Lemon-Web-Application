from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('api/menu/', views.MenuItemsView.as_view(), name="menuitem-list"),
    path('api/menu/<int:pk>', views.SingleMenuItemView.as_view(),
         name="menuitem-detail"),

    path('api/book/', views.BookingView.as_view(), name="booking-list"),
    path('api/book/<int:pk>', views.SingleBookingView.as_view(),
         name="booking-detail"),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
