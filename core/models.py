from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model to handle Roles 
class User(AbstractUser):
    IS_CUSTOMER = 'customer'
    IS_STAFF = 'staff'
    IS_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (IS_CUSTOMER, 'Passenger'),
        (IS_STAFF, 'Airline Staff'),
        (IS_ADMIN, 'Administrator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=IS_CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True) # [cite: 31]

# 2. Aircraft Configuration [cite: 30]
class Aircraft(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    total_economy_seats = models.IntegerField()
    total_business_seats = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"

class Flight(models.Model):
    # Status Choices
    STATUS_CHOICES = [
        ('ON TIME', 'On Time'),
        ('DELAYED', 'Delayed'),
        ('BOARDING', 'Boarding'),
        ('DEPARTED', 'Departed'),
        ('CANCELLED', 'Cancelled'),
    ]

    flight_number = models.CharField(max_length=20, unique=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # NEW FIELDS
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ON TIME')
    gate = models.CharField(max_length=10, default='-')

    def __str__(self):
        return f"{self.flight_number}: {self.origin} to {self.destination}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    # NEW FIELD: To store the actual traveler's name
    passenger_name = models.CharField(max_length=100, default="Unknown") 
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=20) 
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    booked_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.seat_number}"