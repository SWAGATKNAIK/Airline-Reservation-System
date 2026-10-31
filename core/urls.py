from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Auth
    path('signup/', views.customer_signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # Custom Admin
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/flights/', views.admin_flight_list, name='admin_flight_list'),
    path('dashboard/admin/flights/add/', views.admin_flight_add, name='admin_flight_add'),
    path('dashboard/admin/flights/edit/<int:flight_id>/', views.admin_flight_edit, name='admin_flight_edit'),
    path('dashboard/admin/flights/delete/<int:flight_id>/', views.admin_flight_delete, name='admin_flight_delete'),

    # Aircraft Management
    path('dashboard/admin/aircraft/', views.admin_aircraft_list, name='admin_aircraft_list'),
    path('dashboard/admin/aircraft/add/', views.admin_aircraft_add, name='admin_aircraft_add'),
    path('dashboard/admin/aircraft/edit/<int:aircraft_id>/', views.admin_aircraft_edit, name='admin_aircraft_edit'),
    path('dashboard/admin/aircraft/delete/<int:aircraft_id>/', views.admin_aircraft_delete, name='admin_aircraft_delete'),


    # Admin: Staff Management
    path('dashboard/admin/staff/', views.admin_staff_list, name='admin_staff_list'),
    path('dashboard/admin/staff/add/', views.admin_staff_add, name='admin_staff_add'),
    path('dashboard/admin/staff/edit/<int:staff_id>/', views.admin_staff_edit, name='admin_staff_edit'),
    path('dashboard/admin/staff/delete/<int:staff_id>/', views.admin_staff_delete, name='admin_staff_delete'),

    # Staff Interface
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'), # New Summary Dashboard
    path('dashboard/staff/check-in-manager/', views.staff_checkin_manager, name='staff_checkin_manager'), # Old Dashboard (Operations)
    path('dashboard/staff/search/', views.staff_search_passenger, name='staff_search_passenger'), # New Search
    path('dashboard/staff/flight/<int:flight_id>/passengers/', views.staff_flight_passengers, name='staff_flight_passengers'),


    # Admin: Passenger Management
    path('dashboard/admin/passengers/', views.admin_passenger_list, name='admin_passenger_list'),
    path('dashboard/admin/passengers/add/', views.admin_passenger_add, name='admin_passenger_add'),
    path('dashboard/admin/passengers/edit/<int:passenger_id>/', views.admin_passenger_edit, name='admin_passenger_edit'),
    path('dashboard/admin/passengers/delete/<int:passenger_id>/', views.admin_passenger_delete, name='admin_passenger_delete'),

    path('search/', views.search_flights, name='search_flights'),

    path('book/<int:flight_id>/seats/', views.book_flight_seats, name='book_flight_seats'),
    path('book/<int:flight_id>/details/', views.book_passenger_details, name='book_passenger_details'),
    path('book/<int:flight_id>/payment/', views.book_payment, name='book_payment'),
    path('book/success/<int:booking_count>/', views.book_success, name='book_success'),

     # Admin Reservation & Tickets
    path('dashboard/admin/reservations/', views.admin_reservation_list, name='admin_reservation_list'),
    path('dashboard/admin/ticket/<str:booking_id>/', views.admin_boarding_pass, name='admin_boarding_pass'),

    path('my-bookings/', views.customer_bookings, name='customer_bookings'),
    path('my-ticket/<str:booking_id>/', views.customer_boarding_pass, name='customer_boarding_pass'),
    path('cancel-booking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('dashboard/staff/checkin/<int:reservation_id>/', views.staff_toggle_checkin, name='staff_toggle_checkin'),
    path('dashboard/staff/print-ticket/<int:reservation_id>/', views.staff_boarding_pass, name='staff_boarding_pass'),
    path('dashboard/staff/update-flight/<int:flight_id>/', views.staff_update_flight, name='staff_update_flight'),
    
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),


    
]