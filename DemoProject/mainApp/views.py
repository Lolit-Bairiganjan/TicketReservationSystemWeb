from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlencode
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from datetime import datetime, timedelta
import json
from collections import defaultdict
from decimal import Decimal

# Import models
from .models import (
    Station, Train, TrainRoute, TrainSchedule, 
    Coach, Ticket, Passenger, Fare, Payment
)

# Import forms
from .forms import (
    DestinationSelectionForm,
    PassengerBookingForm,
    PassengerForm,
    PassengerFormSet,
    PNRSearchForm,
    SearchForm
)

# Create your views here.
def check_login(view_func):
    """Decorator to check if user is logged in"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue')
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return wrapper


def main_page(request):
    """Main landing page"""
    return render(request, 'mainApp/home.html')


def login_page(request):
    """Display login page"""
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'mainApp/login_page.html')


def login_user(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('main_page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_page')
    
    return redirect('login_page')


def logout_user(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('main_page')


def signup_page(request):
    """Display signup page"""
    if request.user.is_authenticated:
        return redirect('main_page')
    return render(request, 'mainApp/signup_page.html')


def register_user(request):
    """Handle user registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return redirect('signup_page')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_page')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long')
            return redirect('signup_page')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup_page')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup_page')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login_page')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('signup_page')
    
    return redirect('signup_page')


def features_page(request):
    """Display features page"""
    return render(request, 'mainApp/features_page.html')


def contacts_page(request):
    """Display contacts page"""
    return render(request, 'mainApp/contacts_page.html')


@check_login
def select_destinations(request):
    """Handle train and destination selection"""
    if request.method == 'POST':
        train_id = request.POST.get('train')
        journey_date = request.POST.get('journey_date')
        from_station_id = request.POST.get('from_station')
        to_station_id = request.POST.get('to_station')
        
        # Validate all fields are present
        if not all([train_id, journey_date, from_station_id, to_station_id]):
            messages.error(request, 'Please fill all required fields')
            form = DestinationSelectionForm()
            return render(request, 'mainApp/select_destinations.html', {'form': form})
        
        # Validate from and to stations are different
        if from_station_id == to_station_id:
            messages.error(request, 'Source and destination stations must be different')
            form = DestinationSelectionForm()
            return render(request, 'mainApp/select_destinations.html', {'form': form})
        
        # Store in session
        request.session['journey_date'] = journey_date
        
        # Redirect to schedule list with query parameter for date
        return redirect(f"{reverse('schedule_list', args=[train_id, from_station_id, to_station_id])}?date={journey_date}")
    
    # GET request
    form = DestinationSelectionForm()
    return render(request, 'mainApp/select_destinations.html', {'form': form})


@check_login
def schedule_list(request, train_id, from_station_id, to_station_id):
    """Display available schedules for selected train and route"""
    train = get_object_or_404(Train, id=train_id)
    from_station = get_object_or_404(Station, id=from_station_id)
    to_station = get_object_or_404(Station, id=to_station_id)
    
    # Get journey date from query params or session
    journey_date = request.GET.get('date') or request.session.get('journey_date')
    
    # Filter schedules
    if journey_date:
        schedules = TrainSchedule.objects.filter(
            train=train,
            journey_date=journey_date,
            status='SCHEDULED'
        ).select_related('train')
    else:
        # Show next 7 days if no date specified
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)
        schedules = TrainSchedule.objects.filter(
            train=train,
            journey_date__gte=today,
            journey_date__lte=next_week,
            status='SCHEDULED'
        ).select_related('train').order_by('journey_date')
    
    context = {
        'train': train,
        'from_station': from_station,
        'to_station': to_station,
        'schedules': schedules,
        'journey_date': journey_date,
    }
    
    return render(request, 'mainApp/schedule_list.html', context)


@check_login
def select_schedule(request, schedule_id, from_station_id, to_station_id):
    """Store selected schedule in session and redirect to booking"""
    # Clear previous ticket when selecting new schedule
    request.session.pop('current_ticket_id', None)
    
    request.session['schedule_id'] = schedule_id
    request.session['from_station_id'] = from_station_id
    request.session['to_station_id'] = to_station_id
    
    # Redirect with URL parameters
    return redirect('book_ticket', schedule_id=schedule_id, from_station_id=from_station_id, to_station_id=to_station_id)


@check_login
def book_ticket(request, schedule_id, from_station_id, to_station_id):
    """Handle ticket booking with passenger details"""
    schedule = get_object_or_404(TrainSchedule, id=schedule_id)
    from_station = get_object_or_404(Station, id=from_station_id)
    to_station = get_object_or_404(Station, id=to_station_id)
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        seat_class = request.POST.get('seat_class')
        coach_id = request.POST.get('coach')
        berth_preference = request.POST.get('berth_preference')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        
        try:
            # Validate inputs
            if not all([name, age, gender, seat_class]):
                messages.error(request, 'Please fill all required fields')
                return redirect('book_ticket', schedule_id, from_station_id, to_station_id)

            # Prevent the same person from holding multiple seats on this schedule
            if Passenger.objects.filter(
                ticket__schedule=schedule,
                ticket__booking_status__in=['CONFIRMED', 'PENDING'],
                name__iexact=name
            ).exclude(current_status='CANCELLED').exists():
                messages.error(request, f'{name} already has a seat booked for this journey.')
                return redirect('book_ticket', schedule_id, from_station_id, to_station_id)

            # Get the coach
            coach = None
            if coach_id:
                coach = get_object_or_404(Coach, id=coach_id, train=schedule.train)
            else:
                # Auto-assign coach if not selected
                coach = Coach.objects.filter(
                    train=schedule.train,
                    coach_type=seat_class
                ).order_by('-id').first()
            
            if not coach:
                messages.error(request, f'No coach available for {seat_class} class')
                return redirect('book_ticket', schedule_id, from_station_id, to_station_id)
            
            # Check if coach has available seats
            if coach.available_seats <= 0:
                messages.error(request, f'Coach {coach.coach_number} is fully booked. Please select another coach.')
                return redirect('book_ticket', schedule_id, from_station_id, to_station_id)
            
            # Calculate fare
            try:
                fare_obj = Fare.objects.get(
                    train=schedule.train,
                    source_station=from_station,
                    destination_station=to_station
                )
                base_fare = fare_obj.base_fare
            except Fare.DoesNotExist:
                base_fare = schedule.base_fare
            
            # Class-based fare multipliers
            class_multipliers = {
                'GENERAL': Decimal('1.0'),
                'SLEEPER': Decimal('1.5'),
                'AC_3_TIER': Decimal('2.0'),
                'AC_2_TIER': Decimal('3.0'),
                'AC_1_TIER': Decimal('5.0'),
                'FIRST_CLASS': Decimal('6.0'),
            }
            
            passenger_fare = base_fare * class_multipliers.get(seat_class, Decimal('1.0'))
            
            # Check if adding to existing ticket or creating new
            current_ticket_id = request.session.get('current_ticket_id')
            
            if current_ticket_id:
                # Adding passenger to existing ticket
                ticket = get_object_or_404(Ticket, id=current_ticket_id, booking_status='CONFIRMED')
                # Update total fare
                ticket.total_fare += passenger_fare
                ticket.save()
            else:
                # Create new ticket
                ticket = Ticket.objects.create(
                    schedule=schedule,
                    passenger_name=name,
                    email=email,
                    seat_class=seat_class,
                    source_station=from_station,
                    destination_station=to_station,
                    booking_status='CONFIRMED',
                    total_fare=passenger_fare
                )
                request.session['current_ticket_id'] = ticket.id
            
            # Create passenger with calculated fare
            passenger = Passenger.objects.create(
                ticket=ticket,
                name=name,
                age=age,
                gender=gender,
                seat_class=seat_class,
                fare=passenger_fare,  # Save the fare
                coach=coach,
                current_status='CONFIRMED'
            )
            
            # Assign seat based on berth preference
            passenger.save(berth_preference=berth_preference)
            
            messages.success(request, f'Passenger {name} added successfully! Seat: {coach.coach_number}-{passenger.seat_number}')
            return redirect('ticket_detail', pnr=ticket.pnr)
            
        except Exception as e:
            messages.error(request, f'Error booking ticket: {str(e)}')
            return redirect('book_ticket', schedule_id, from_station_id, to_station_id)
    
    # GET request - show booking form
    # Get available coaches grouped by class
    coaches_by_class = defaultdict(list)
    available_classes = set()
    
    for coach in schedule.train.coaches.all():
        available_classes.add(coach.coach_type)
        coaches_by_class[coach.coach_type].append({
            'id': coach.id,
            'number': coach.coach_number,
            'available': coach.available_seats,
            'total': coach.total_seats,
            'type': coach.get_coach_type_display()
        })
    
    # Create seat class choices with display names
    CLASS_DISPLAY = {
        'GENERAL': 'General',
        'SLEEPER': 'Sleeper',
        'AC_3_TIER': 'AC 3 Tier',
        'AC_2_TIER': 'AC 2 Tier',
        'AC_1_TIER': 'AC 1 Tier',
        'FIRST_CLASS': 'First Class',
    }
    
    available_seat_classes = [
        {'value': cls, 'display': CLASS_DISPLAY.get(cls, cls)}
        for cls in available_classes
    ]
    
    context = {
        'schedule': schedule,
        'from_station': from_station,
        'to_station': to_station,
        'coaches_by_class': json.dumps(dict(coaches_by_class)),
        'available_seat_classes': available_seat_classes,
    }
    
    return render(request, 'mainApp/book_ticket.html', context)


@check_login
def ticket_detail(request, pnr):
    """Display ticket details"""
    ticket = get_object_or_404(Ticket, pnr=pnr)
    return render(request, 'mainApp/ticket_detail.html', {'ticket': ticket})


@check_login
def add_passengers(request, pnr):
    """Add more passengers to an existing ticket"""
    ticket = get_object_or_404(Ticket, pnr=pnr, booking_status='CONFIRMED')
    
    # Set session variables from the ticket
    schedule_id = ticket.schedule.id
    from_station_id = ticket.source_station.id if ticket.source_station else None
    to_station_id = ticket.destination_station.id if ticket.destination_station else None
    
    request.session['schedule_id'] = schedule_id
    request.session['from_station_id'] = from_station_id
    request.session['to_station_id'] = to_station_id
    request.session['current_ticket_id'] = ticket.id
    
    # Redirect with URL parameters
    return redirect('book_ticket', schedule_id=schedule_id, from_station_id=from_station_id, to_station_id=to_station_id)


@check_login
def cancel_ticket(request, pnr):
    """Cancel a ticket"""
    ticket = get_object_or_404(Ticket, pnr=pnr)
    
    if ticket.booking_status == 'CANCELLED':
        messages.warning(request, 'This ticket is already cancelled')
        return redirect('ticket_detail', pnr=pnr)
    
    if request.method == 'POST':
        ticket.booking_status = 'CANCELLED'
        ticket.save()
        
        # Update all passengers to cancelled
        ticket.passengers.all().update(current_status='CANCELLED')
        
        messages.success(request, f'Ticket {pnr} has been cancelled successfully')
        return redirect('ticket_detail', pnr=pnr)
    
    return render(request, 'mainApp/cancel_ticket.html', {'ticket': ticket})


@check_login
def check_pnr_status(request):
    """Check PNR status"""
    if request.method == 'POST':
        pnr = request.POST.get('pnr', '').strip().upper()
        
        if not pnr:
            messages.error(request, 'Please enter a PNR number')
            return render(request, 'mainApp/check_pnr.html')
        
        try:
            ticket = Ticket.objects.get(pnr=pnr)
            # Redirect to ticket detail page instead of separate PNR status page
            return redirect('ticket_detail', pnr=pnr)
        except Ticket.DoesNotExist:
            messages.error(request, f'No ticket found with PNR: {pnr}')
            return render(request, 'mainApp/check_pnr.html')
    
    return render(request, 'mainApp/check_pnr.html')


@check_login
def clear_ticket_session(request):
    """Clear ticket session data"""
    request.session.pop('current_ticket_id', None)
    request.session.pop('schedule_id', None)
    request.session.pop('from_station_id', None)
    request.session.pop('to_station_id', None)
    messages.success(request, 'Session cleared')
    return redirect('select_destinations')

