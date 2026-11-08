from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib import messages
import uuid
from django.db.models import Q 

from datetime import timedelta
# --- Public Views ---
def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def contact(request):
    return render(request, 'public/contact.html')

# --- Authentication Views ---
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Redirect to home after signup
    else:
        form = CustomerSignUpForm()
    return render(request, 'public/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # FIX: Check if 'next' parameter exists (e.g. from clicking Book Now)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Default Role-based Redirection
            if user.is_superuser or user.role == User.IS_ADMIN:
                return redirect('admin_dashboard')
            elif user.role == User.IS_STAFF:
                return redirect('staff_dashboard')
            else:
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'public/login.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('login')

# --- Admin Views ---
# Check if user is admin or superuser
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == User.IS_ADMIN)

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    # Fetch stats for the dashboard
    context = {
        'total_flights': Flight.objects.count(),
        'total_passengers': User.objects.filter(role=User.IS_CUSTOMER, is_superuser=False).count(),
        'total_reservations': Reservation.objects.count(),
        'recent_reservations': Reservation.objects.order_by('-booked_at')[:5]
    }
    return render(request, 'custom_admin/dashboard.html', context)


@user_passes_test(is_admin, login_url='login')
def admin_flight_list(request):
    flights = Flight.objects.all().order_by('-departure_time')
    return render(request, 'custom_admin/flight_list.html', {'flights': flights})

@user_passes_test(is_admin, login_url='login')
def admin_flight_add(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_flight_list')
    else:
        form = FlightForm()
    return render(request, 'custom_admin/flight_form.html', {'form': form, 'title': 'Schedule New Flight'})

@user_passes_test(is_admin, login_url='login')
def admin_flight_edit(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('admin_flight_list')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'custom_admin/flight_form.html', {'form': form, 'title': 'Edit Flight'})

@user_passes_test(is_admin, login_url='login')
def admin_flight_delete(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        flight.delete()
        return redirect('admin_flight_list')
    return render(request, 'custom_admin/flight_confirm_delete.html', {'flight': flight})


@user_passes_test(is_admin, login_url='login')
def admin_aircraft_list(request):
    aircrafts = Aircraft.objects.all()
    return render(request, 'custom_admin/aircraft_list.html', {'aircrafts': aircrafts})

@user_passes_test(is_admin, login_url='login')
def admin_aircraft_add(request):
    if request.method == 'POST':
        form = AircraftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_aircraft_list')
    else:
        form = AircraftForm()
    return render(request, 'custom_admin/aircraft_form.html', {'form': form, 'title': 'Add New Aircraft'})

@user_passes_test(is_admin, login_url='login')
def admin_aircraft_edit(request, aircraft_id):
    aircraft = get_object_or_404(Aircraft, id=aircraft_id)
    if request.method == 'POST':
        form = AircraftForm(request.POST, instance=aircraft)
        if form.is_valid():
            form.save()
            return redirect('admin_aircraft_list')
    else:
        form = AircraftForm(instance=aircraft)
    return render(request, 'custom_admin/aircraft_form.html', {'form': form, 'title': 'Edit Aircraft'})

@user_passes_test(is_admin, login_url='login')
def admin_aircraft_delete(request, aircraft_id):
    aircraft = get_object_or_404(Aircraft, id=aircraft_id)
    if request.method == 'POST':
        aircraft.delete()
        return redirect('admin_aircraft_list')
    return render(request, 'custom_admin/aircraft_confirm_delete.html', {'aircraft': aircraft})


@user_passes_test(is_admin, login_url='login')
def admin_staff_list(request):
    staff_members = User.objects.filter(role=User.IS_STAFF)
    return render(request, 'custom_admin/staff_list.html', {'staff_members': staff_members})

@user_passes_test(is_admin, login_url='login')
def admin_staff_add(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_staff_list')
    else:
        form = StaffCreationForm()
    return render(request, 'custom_admin/staff_form.html', {'form': form, 'title': 'Register New Staff'})

@user_passes_test(is_admin, login_url='login')
def admin_staff_edit(request, staff_id):
    staff = get_object_or_404(User, id=staff_id)
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('admin_staff_list')
    else:
        form = StaffEditForm(instance=staff)
    return render(request, 'custom_admin/staff_form.html', {'form': form, 'title': 'Edit Staff Details'})

@user_passes_test(is_admin, login_url='login')
def admin_staff_delete(request, staff_id):
    staff = get_object_or_404(User, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('admin_staff_list')
    return render(request, 'custom_admin/staff_confirm_delete.html', {'staff': staff})


# --- Staff Interface ---

def is_staff_user(user):
    return user.is_authenticated and user.role == User.IS_STAFF




@user_passes_test(is_staff_user, login_url='login')
def staff_dashboard(request):
    # NEW DASHBOARD: Shows High-Level "Today's Overview"
    # FIX: Use full datetime object (now) instead of just .date() so template can show time (H:i)
    now = timezone.now()
    
    # Filter flights for the next 24 hours
    todays_flights = Flight.objects.filter(
        departure_time__gte=now,
        departure_time__lt=now + timedelta(hours=24)
    ).order_by('departure_time')

    # Quick Stats
    total_flights_today = todays_flights.count()
    passengers_today = Reservation.objects.filter(flight__in=todays_flights, status='CONFIRMED').count()
    checked_in_today = Reservation.objects.filter(flight__in=todays_flights, status='CONFIRMED', is_checked_in=True).count()
    delayed_flights = todays_flights.filter(status='DELAYED').count()

    context = {
        'flights': todays_flights,
        'total_flights': total_flights_today,
        'passengers_today': passengers_today,
        'checked_in_count': checked_in_today, # FIXED: Changed key from 'checked_in_today' to 'checked_in_count' to match template
        'delayed_flights': delayed_flights,
        'today_date': now
    }
    return render(request, 'staff/dashboard.html', context)
@user_passes_test(is_staff_user, login_url='login')
def staff_checkin_manager(request):
    # OLD DASHBOARD LOGIC (Moved here): Flight Cards for Operations
    flights = Flight.objects.filter(departure_time__gte=timezone.now()).order_by('departure_time')
    
    for flight in flights:
        flight.total_booked = Reservation.objects.filter(flight=flight, status='CONFIRMED').count()
        flight.checked_in_count = Reservation.objects.filter(flight=flight, status='CONFIRMED', is_checked_in=True).count()
        flight.capacity = flight.aircraft.total_economy_seats + flight.aircraft.total_business_seats

    return render(request, 'staff/checkin_list.html', {'flights': flights})

@user_passes_test(is_staff_user, login_url='login')
def staff_search_passenger(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        # Search by PNR, Name, Seat, or Flight Number
        results = Reservation.objects.filter(
            Q(booking_id__icontains=query) | 
            Q(passenger_name__icontains=query) |
            Q(seat_number__icontains=query) |
            Q(flight__flight_number__icontains=query)
        ).filter(status='CONFIRMED').order_by('-flight__departure_time')

    return render(request, 'staff/search_passenger.html', {'query': query, 'results': results})

@user_passes_test(is_staff_user, login_url='login')
def staff_flight_passengers(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    # Get all confirmed passengers
    reservations = Reservation.objects.filter(flight=flight, status='CONFIRMED').order_by('seat_number')
    return render(request, 'staff/passenger_list.html', {'flight': flight, 'reservations': reservations})

@user_passes_test(is_staff_user, login_url='login')
def staff_toggle_checkin(request, reservation_id):
    # Staff clicks "Check In" button
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.is_checked_in = not reservation.is_checked_in # Toggle True/False
    reservation.save()
    messages.success(request, f"Check-in status updated for {reservation.passenger_name}")
    return redirect('staff_flight_passengers', flight_id=reservation.flight.id)

@user_passes_test(is_staff_user, login_url='login')
def staff_boarding_pass(request, reservation_id):
    # Allow staff to print boarding pass for a specific passenger
    ticket = get_object_or_404(Reservation, id=reservation_id)
    # Reuse the admin boarding pass template (pass as a list to match template loop)
    return render(request, 'custom_admin/boarding_pass.html', {'tickets': [ticket]})

@user_passes_test(is_admin, login_url='login')
def admin_passenger_list(request):
    passengers = User.objects.filter(role=User.IS_CUSTOMER).exclude(is_superuser=True).exclude(is_staff=True)
    return render(request, 'custom_admin/passenger_list.html', {'passengers': passengers})

@user_passes_test(is_admin, login_url='login')
def admin_passenger_add(request):
    if request.method == 'POST':
        form = PassengerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_passenger_list')
    else:
        form = PassengerCreationForm()
    return render(request, 'custom_admin/passenger_form.html', {'form': form, 'title': 'Register New Passenger'})

@user_passes_test(is_admin, login_url='login')
def admin_passenger_edit(request, passenger_id):
    passenger = get_object_or_404(User, id=passenger_id)
    if request.method == 'POST':
        form = PassengerEditForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return redirect('admin_passenger_list')
    else:
        form = PassengerEditForm(instance=passenger)
    return render(request, 'custom_admin/passenger_form.html', {'form': form, 'title': 'Edit Passenger Details'})

@user_passes_test(is_admin, login_url='login')
def admin_passenger_delete(request, passenger_id):
    passenger = get_object_or_404(User, id=passenger_id)
    if request.method == 'POST':
        passenger.delete()
        return redirect('admin_passenger_list')
    return render(request, 'custom_admin/passenger_confirm_delete.html', {'passenger': passenger})




def search_flights(request):
    form = FlightSearchForm(request.GET or None)
    flights = []
    searched = False

    if request.GET and form.is_valid():
        searched = True
        origin = form.cleaned_data['origin']
        destination = form.cleaned_data['destination']
        date = form.cleaned_data['date']
        
        # Get the QuerySet
        flight_qs = Flight.objects.filter(
            origin__icontains=origin,
            destination__icontains=destination,
            departure_time__date=date
        ).order_by('base_price')

        # FIX: Iterate and calculate available seats
        flights = []
        for flight in flight_qs:
            booked_count = Reservation.objects.filter(flight=flight, status='CONFIRMED').count()
            # Attach a temporary attribute 'available_seats' to the object
            flight.available_seats = flight.aircraft.total_economy_seats - booked_count
            flights.append(flight)

    return render(request, 'public/flight_search.html', {
        'form': form, 
        'flights': flights, 
        'searched': searched
    })


# ==========================================
#       NEW BOOKING LOGIC STARTS HERE
# ==========================================

@login_required(login_url='login')
def book_flight_seats(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Get all currently booked seats for this flight
    booked_seats = Reservation.objects.filter(flight=flight, status='CONFIRMED').values_list('seat_number', flat=True)
    
    # Generate Seat Map Configuration
    # Assuming 6 seats per row (ABC - DEF)
    total_seats = flight.aircraft.total_economy_seats
    rows = (total_seats // 6) + (1 if total_seats % 6 > 0 else 0)
    
    seat_map = []
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    
    current_seat_count = 0
    for row in range(1, rows + 1):
        row_seats = []
        for letter in seat_letters:
            current_seat_count += 1
            if current_seat_count > total_seats:
                break
                
            seat_label = f"{row}{letter}"
            is_booked = seat_label in booked_seats
            row_seats.append({
                'label': seat_label,
                'is_booked': is_booked
            })
        seat_map.append({'row_num': row, 'seats': row_seats})

    if request.method == 'POST':
        selected_seats = request.POST.get('selected_seats') # Comma separated string "1A,1B"
        if selected_seats:
            # Save selection to session
            request.session['booking_seats'] = selected_seats.split(',')
            return redirect('book_passenger_details', flight_id=flight.id)
        else:
            messages.error(request, "Please select at least one seat.")

    return render(request, 'public/booking_seat_select.html', {
        'flight': flight,
        'seat_map': seat_map
    })

@login_required(login_url='login')
def book_passenger_details(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    selected_seats = request.session.get('booking_seats', [])
    
    if not selected_seats:
        return redirect('book_flight_seats', flight_id=flight.id)

    if request.method == 'POST':
        # Collect passenger names
        passenger_data = []
        for seat in selected_seats:
            name = request.POST.get(f'passenger_name_{seat}')
            if name:
                passenger_data.append({'seat': seat, 'name': name})
        
        # Save detailed data to session for payment page
        request.session['booking_passengers'] = passenger_data
        return redirect('book_payment', flight_id=flight.id)

    return render(request, 'public/booking_details.html', {
        'flight': flight,
        'selected_seats': selected_seats
    })


@login_required(login_url='login')
def book_payment(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    passenger_data = request.session.get('booking_passengers', [])
    
    # Redirect if no session data found
    if not passenger_data:
        return redirect('book_flight_seats', flight_id=flight.id)

    total_price = flight.base_price * len(passenger_data)

    if request.method == 'POST':
        # FIX: Generate ONE Booking ID (PNR) for the whole group
        # This ensures all 3 seats (if selected) share the same Booking Ref
        pnr = str(uuid.uuid4())[:6].upper() 
        
        booked_count = 0
        for p in passenger_data:
            Reservation.objects.create(
                passenger=request.user,
                passenger_name=p['name'],
                flight=flight,
                booking_id=pnr, # Use the shared PNR here
                seat_number=p['seat'],
                status='CONFIRMED'
            )
            booked_count += 1
        
        # Clear session
        if 'booking_seats' in request.session:
            del request.session['booking_seats']
        if 'booking_passengers' in request.session:
            del request.session['booking_passengers']
        
        return redirect('book_success', booking_count=booked_count)

    return render(request, 'public/booking_payment.html', {
        'flight': flight,
        'passenger_data': passenger_data,
        'total_price': total_price
    })
@login_required(login_url='login')
def book_success(request, booking_count):
    return render(request, 'public/booking_success.html', {'count': booking_count})



@user_passes_test(is_admin, login_url='login')
def admin_reservation_list(request):
    query = request.GET.get('q')
    reservations = Reservation.objects.all().order_by('-booked_at')
    
    if query:
        # Search by Passenger Name, Flight Number, Booking ID, or Date (YYYY-MM-DD)
        reservations = reservations.filter(
            Q(passenger_name__icontains=query) | 
            Q(booking_id__icontains=query) |
            Q(flight__flight_number__icontains=query) |
            Q(flight__departure_time__date__icontains=query)
        )

    # We want to group by Booking ID to show distinct transactions, 
    # but Django templates handle loops well. 
    # Let's pass the raw list and handle grouping in template or show individual rows.
    # Showing individual rows is better for searching specific names.
    
    return render(request, 'custom_admin/reservation_list.html', {
        'reservations': reservations,
        'query': query
    })

@user_passes_test(is_admin, login_url='login')
def admin_boarding_pass(request, booking_id):
    # Fetch all seats under this Booking ID (PNR)
    tickets = Reservation.objects.filter(booking_id=booking_id)
    
    if not tickets.exists():
        return redirect('admin_reservation_list')
        
    return render(request, 'custom_admin/boarding_pass.html', {'tickets': tickets})


@login_required(login_url='login')
def customer_bookings(request):
    # Filter bookings only for the logged-in user
    bookings = Reservation.objects.filter(passenger=request.user).order_by('-booked_at')
    return render(request, 'public/my_bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def customer_boarding_pass(request, booking_id):
    # Security Check: Ensure booking belongs to user AND is CONFIRMED
    tickets = Reservation.objects.filter(booking_id=booking_id, passenger=request.user, status='CONFIRMED')
    
    if not tickets.exists():
        # Check if it exists but is cancelled
        cancelled_check = Reservation.objects.filter(booking_id=booking_id, passenger=request.user, status='CANCELLED')
        if cancelled_check.exists():
            messages.error(request, "This booking has been cancelled. Ticket is no longer valid.")
        else:
            messages.error(request, "Ticket not found or access denied.")
        return redirect('customer_bookings')
        
    return render(request, 'custom_admin/boarding_pass.html', {'tickets': tickets})


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    # Fetch valid bookings for this PNR
    reservations = Reservation.objects.filter(booking_id=booking_id, passenger=request.user, status='CONFIRMED')

    if not reservations.exists():
        messages.error(request, "Active booking not found.")
        return redirect('customer_bookings')

    flight = reservations.first().flight
    
    # Logic: Check if flight is at least 5 hours away
    current_time = timezone.now()
    time_until_departure = flight.departure_time - current_time
    hours_left = time_until_departure.total_seconds() / 3600

    if hours_left < 5:
        messages.error(request, "Cancellations are only allowed up to 5 hours before departure.")
        return redirect('customer_bookings')

    # Calculate Refund
    ticket_count = reservations.count()
    total_paid = flight.base_price * ticket_count
    
    # Example: ₹1000 fee per passenger
    cancellation_fee = 1000 * ticket_count 
    refund_amount = total_paid - cancellation_fee
    
    # Ensure refund isn't negative
    if refund_amount < 0: 
        refund_amount = 0
        cancellation_fee = total_paid

    if request.method == 'POST':
        # Process Cancellation
        # Changing status to 'CANCELLED' automatically frees up seats in search results
        # because search results filter by 'CONFIRMED'.
        reservations.update(status='CANCELLED')
        
        messages.success(request, f"Booking {booking_id} cancelled successfully. ₹{refund_amount} will be refunded within 2-3 business days.")
        return redirect('customer_bookings')

    return render(request, 'public/cancel_booking.html', {
        'reservations': reservations,
        'flight': flight,
        'booking_id': booking_id,
        'total_paid': total_paid,
        'cancellation_fee': cancellation_fee,
        'refund_amount': refund_amount,
        'ticket_count': ticket_count
    })


@user_passes_test(is_staff_user, login_url='login')
def staff_update_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        form = FlightStatusForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, f"Flight {flight.flight_number} updated: Status is {flight.get_status_display()} at Gate {flight.gate}")
            return redirect('staff_dashboard')
    else:
        form = FlightStatusForm(instance=flight)
        
    return render(request, 'staff/flight_update.html', {'form': form, 'flight': flight})


import re
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- CHATBOT INTEGRATION ---



@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip().lower()
        except json.JSONDecodeError:
            return JsonResponse({'response': "Invalid data format."})

        response_text = "I'm sorry, I didn't quite catch that. Try asking 'Flights to Mumbai' or 'Check PNR 123456'."

        # ====================================================
        # INTENT DETECTION
        # ====================================================
        
        # Keywords that indicate the user is asking about a booking
        booking_keywords = ['pnr', 'booking', 'reservation', 'ticket', 'boarding', 'status', 'check in', 'details']
        is_booking_intent = any(kw in user_message for kw in booking_keywords)
        
        # Extract potential PNRs (6-character alphanumeric)
        # We filter out common words that happen to be 6 letters long to avoid false PNR detection
        ignore_words = {
            'flight', 'search', 'cancel', 'booker', 'system', 'return', 'refund', 'please', 'travel', 
            'thanks', 'hello', 'assist', 'create', 'update', 'delete', 'remove', 'detail', 'ticket', 'status', 'check'
        }
        
        potential_pnrs = re.findall(r'\b[a-z0-9]{6}\b', user_message)
        valid_pnrs = [p for p in potential_pnrs if p not in ignore_words]
        
        # ====================================================
        # LOGIC 1: HANDLE BOOKING QUERIES
        # ====================================================
        
        if valid_pnrs:
            # Case A: User provided something that looks like a PNR
            for pnr in valid_pnrs:
                booking = Reservation.objects.filter(booking_id__iexact=pnr).first()
                if booking:
                    status_badge = "info"
                    if booking.status == 'CONFIRMED': status_badge = "success"
                    elif booking.status == 'CANCELLED': status_badge = "danger"

                    response_text = (
                        f"Found it! <br>"
                        f"<strong>PNR: {booking.booking_id.upper()}</strong> <span class='badge bg-{status_badge}'>{booking.status}</span><br>"
                        f"👤 Passenger: {booking.passenger_name}<br>"
                        f"✈️ Flight: {booking.flight.flight_number}<br>"
                        f"📅 Date: {booking.flight.departure_time.strftime('%d %b %Y, %H:%M')}<br>"
                        f"📍 Route: {booking.flight.origin} ➝ {booking.flight.destination}"
                    )
                    return JsonResponse({'response': response_text})
            
            # If we reached here, PNRs were found in text but none matched in DB
            return JsonResponse({'response': f"I couldn't find any booking with PNR <strong>{valid_pnrs[0].upper()}</strong>. Please check the ID and try again."})

        elif is_booking_intent:
            # Case B: User asked about booking ("my ticket", "booking status") but didn't provide a valid 6-char PNR
            return JsonResponse({'response': "To check your booking, please provide your 6-character <strong>PNR</strong> (e.g., 17D232)."})

        # ====================================================
        # LOGIC 2: FLIGHT SEARCH (Default Fallback)
        # ====================================================
        
        # Only proceed to flight search if it wasn't a booking intent
        
        # --- Extract Date ---
        search_date = timezone.now().date() # Default to today
        date_label = "today"
        if "tomorrow" in user_message:
            search_date = search_date + timedelta(days=1)
            date_label = "tomorrow"
        
        # --- Extract Locations ---
        origin = None
        destination = None
        
        # Regex for explicit "from X to Y"
        route_match = re.search(r'from\s+(\w+)\s+to\s+(\w+)', user_message)
        
        if route_match:
            origin = route_match.group(1)
            destination = route_match.group(2)
        else:
            # Regex for "to [City]" or "for [City]"
            dest_match = re.search(r'(?:to|for)\s+(\w+)', user_message)
            if dest_match:
                destination = dest_match.group(1)
            
            # Regex for "from [City]"
            origin_match = re.search(r'from\s+(\w+)', user_message)
            if origin_match:
                origin = origin_match.group(1)

        # --- Build Query ---
        flights = Flight.objects.filter(departure_time__date=search_date)
        
        query_desc = ""
        
        if origin and destination:
            flights = flights.filter(origin__icontains=origin, destination__icontains=destination)
            query_desc = f"from {origin} to {destination}"
        elif origin:
            flights = flights.filter(origin__icontains=origin)
            query_desc = f"departing from {origin}"
        elif destination:
            flights = flights.filter(destination__icontains=destination)
            query_desc = f"arriving in {destination}"
        else:
            # Fallback: If no prepositions (e.g. "Pune flight"), search for city in both fields
            flight_keywords = ["flight", "fly", "travel", "go to", "from", "to", "show", "me"]
            words = user_message.split()
            city_candidates = [w for w in words if w not in flight_keywords and len(w) > 3]
            
            if city_candidates:
                search_term = city_candidates[0] # Take the first significant word
                flights = flights.filter(
                    Q(origin__icontains=search_term) | 
                    Q(destination__icontains=search_term)
                )
                query_desc = f"related to {search_term}"
            else:
                # No city found in query
                return JsonResponse({'response': "Where would you like to fly? Try asking 'Flights to Delhi' or 'From Mumbai to Pune'."})

        # --- Generate Response ---
        if flights.exists():
            flight_list = ""
            for f in flights:
                flight_list += (
                    f"<div class='mt-2 p-2 border rounded bg-white shadow-sm'>"
                    f"<div class='d-flex justify-content-between'>"
                    f"<strong>{f.flight_number}</strong>"
                    f"<span class='text-primary fw-bold'>₹{f.base_price}</span>"
                    f"</div>"
                    f"<small>{f.origin} ➝ {f.destination}</small><br>"
                    f"<small class='text-muted'>🕒 {f.departure_time.strftime('%H:%M')}</small>"
                    f"<a href='/book/{f.id}/seats/' class='btn btn-sm btn-outline-primary w-100 mt-1'>Book</a>"
                    f"</div>"
                )
            response_text = f"Here are the flights {query_desc} for {date_label}: {flight_list}"
        else:
            response_text = f"I couldn't find any flights {query_desc} for {date_label}. Try changing the date or city."

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request'}, status=400)
