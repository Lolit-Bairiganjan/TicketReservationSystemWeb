from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlencode
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date as date_cls
from django.db import transaction
from decimal import Decimal
from .models import Train, Station, TrainSchedule, TrainRoute, Ticket, Passenger, Fare, Coach
from .forms import SearchForm, PassengerFormSet

# Create your views here.
def check_login(requested_view):
    def login_wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to login first to access this content.")
            params = urlencode({'next': request.path})
            return redirect(f"{reverse('login_page')}?{params}")
        result = requested_view(request, *args, **kwargs)
        return result
    return login_wrapper

def main_page(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username = username, password = passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "You're successfully logged in.")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('main_page')
        else:
            messages.error(request, "Login failed. Try again.")
            return redirect('main_page')

def logout_user(request):
    logout(request)
    messages.warning(request, "User logged out.")
    return redirect('main_page')

def features_page(request):
    return render(request, 'features.html')

def contacts_page(request):
    return render(request, 'contact.html')

def signup_page(request):
    return render(request, 'login_signup.html')

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        passwd = request.POST['password']

        # Basic Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup_page")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup_page")
        
        # Create the user (Django hashes the password automatically)
        user = User.objects.create_user(username=username, email=email, password=passwd)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login_page")

@check_login
def check_pnr_status(request):
    ticket = None
    passengers = []
    
    if request.method == 'POST':
        pnr = request.POST.get('pnr', '').strip()
        
        if pnr:
            try:
                ticket = Ticket.objects.get(pnr=pnr)
                passengers = ticket.passengers.all()
                messages.success(request, f"PNR {pnr} found!")
            except Ticket.DoesNotExist:
                messages.error(request, f"No ticket found with PNR: {pnr}")
        else:
            messages.error(request, "Please enter a PNR number")
    
    context = {
        'ticket': ticket,
        'passengers': passengers,
    }
    
    return render(request, 'mainApp/pnr_status.html', context)

@check_login
def select_destinations(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            train = form.cleaned_data['train']
            from_station = form.cleaned_data['from_station']
            to_station = form.cleaned_data['to_station']
            journey_date = form.cleaned_data['journey_date']
            url = reverse('schedule_list', args=[train.id, from_station.id, to_station.id])
            return redirect(f"{url}?date={journey_date}")
    else:
        form = SearchForm()
    return render(request, 'mainApp/select_destinations.html', {'form': form})

@check_login
def schedule_list(request, train_id, from_station_id, to_station_id):
    train = get_object_or_404(Train, id=train_id)
    from_station = get_object_or_404(Station, id=from_station_id)
    to_station = get_object_or_404(Station, id=to_station_id)
    
    date = request.GET.get('date')
    if date:
        schedules = TrainSchedule.objects.filter(
            train=train,
            journey_date=date,
            status='SCHEDULED'
        )
    else:
        schedules = TrainSchedule.objects.filter(
            train=train,
            status='SCHEDULED'
        ).order_by('journey_date')[:7]  # Next 7 days
    
    # Get departure and arrival times from TrainRoute
    from_route = TrainRoute.objects.filter(train=train, station=from_station).first()
    to_route = TrainRoute.objects.filter(train=train, station=to_station).first()
    
    context = {
        'train': train,
        'from_station': from_station,
        'to_station': to_station,
        'schedules': schedules,
        'date': date,
        'departure_time': from_route.departure_time if from_route else None,
        'arrival_time': to_route.arrival_time if to_route else None,
    }
    
    return render(request, 'mainApp/schedule_list.html', context)


@check_login
def select_schedule(request, schedule_id, from_station_id, to_station_id):
    """Store selected schedule in session and redirect to booking"""
    request.session['schedule_id'] = schedule_id
    request.session['from_station_id'] = from_station_id
    request.session['to_station_id'] = to_station_id
    
    return redirect('book_ticket')


@check_login
def book_ticket(request):
    # Get booking details from session
    schedule_id = request.session.get('schedule_id')
    from_station_id = request.session.get('from_station_id')
    to_station_id = request.session.get('to_station_id')
    existing_ticket_id = request.session.get('current_ticket_id')
    
    if not all([schedule_id, from_station_id, to_station_id]):
        messages.error(request, "Please select a train first.")
        return redirect('select_destinations')
    
    schedule = get_object_or_404(TrainSchedule, id=schedule_id)
    from_station = get_object_or_404(Station, id=from_station_id)
    to_station = get_object_or_404(Station, id=to_station_id)
    
    # Get fare
    try:
        fare = Fare.objects.get(
            train=schedule.train,
            source_station=from_station,
            destination_station=to_station
        )
        price = fare.total_fare()
    except Fare.DoesNotExist:
        messages.error(request, "Fare not available for this route.")
        return redirect('select_destinations')
    
    # Check if we're adding to an existing ticket
    existing_ticket = None
    if existing_ticket_id:
        try:
            existing_ticket = Ticket.objects.get(id=existing_ticket_id, booking_status='CONFIRMED')
            # Verify it's for the same schedule
            if existing_ticket.schedule.id != schedule_id:
                existing_ticket = None
                request.session.pop('current_ticket_id', None)
        except Ticket.DoesNotExist:
            existing_ticket = None
            request.session.pop('current_ticket_id', None)
    
    if request.method == 'POST':
        formset = PassengerFormSet(request.POST, form_kwargs={'train': schedule.train})
        
        if formset.is_valid():
            # Check for duplicate passengers on the same schedule
            passenger_names = []
            for form in formset:
                if form.cleaned_data and form.cleaned_data.get('name'):
                    name = form.cleaned_data['name'].strip().lower()
                    
                    # Check if this person already has a ticket on this schedule
                    existing_booking = Passenger.objects.filter(
                        ticket__schedule=schedule,
                        name__iexact=name,
                        ticket__booking_status__in=['CONFIRMED', 'PENDING']
                    ).exists()
                    
                    if existing_booking:
                        messages.error(request, f"Passenger '{form.cleaned_data['name']}' already has a booking on this train for the selected date.")
                        return render(request, 'mainApp/book_ticket.html', {
                            'schedule': schedule,
                            'from_station': from_station,
                            'to_station': to_station,
                            'price': price,
                            'formset': formset,
                            'existing_ticket': existing_ticket,
                        })
                    
                    # Check for duplicate names in the same booking
                    if name in passenger_names:
                        messages.error(request, f"Duplicate passenger name '{form.cleaned_data['name']}' found in the booking.")
                        return render(request, 'mainApp/book_ticket.html', {
                            'schedule': schedule,
                            'from_station': from_station,
                            'to_station': to_station,
                            'price': price,
                            'formset': formset,
                            'existing_ticket': existing_ticket,
                        })
                    
                    passenger_names.append(name)
            
            try:
                with transaction.atomic():
                    # Use existing ticket or create new one
                    if existing_ticket:
                        ticket = existing_ticket
                        total_amount = ticket.total_fare  # Start with existing fare
                    else:
                        # Create new ticket with station info and total_fare
                        total_amount = Decimal('0')
                        ticket = Ticket.objects.create(
                            schedule=schedule,
                            passenger_name=formset.forms[0].cleaned_data['name'],
                            email=request.user.email if request.user.is_authenticated else '',
                            seat_class=formset.forms[0].cleaned_data['seat_class'],
                            source_station=from_station,
                            destination_station=to_station,
                            total_fare=Decimal('0')  # Will be updated after adding passengers
                        )
                        # Store ticket ID in session for future additions
                        request.session['current_ticket_id'] = ticket.id
                    
                    # Create passengers
                    for form in formset:
                        if form.cleaned_data and form.cleaned_data.get('name'):
                            passenger = form.save(commit=False)
                            passenger.ticket = ticket
                            berth_pref = form.cleaned_data.get('berth_preference')
                            if berth_pref:
                                passenger.save(berth_preference=berth_pref)
                            else:
                                passenger.save()
                            total_amount += price
                    
                    # Update total fare
                    ticket.total_fare = total_amount
                    ticket.save()
                    
                    if existing_ticket:
                        messages.success(request, f"Passenger(s) added to PNR: {ticket.pnr}")
                    else:
                        messages.success(request, f"Ticket booked successfully! PNR: {ticket.pnr}")
                    
                    return redirect('ticket_detail', pnr=ticket.pnr)
                    
            except Exception as e:
                messages.error(request, f"Booking failed: {str(e)}")
        else:
            # Show detailed errors
            messages.error(request, "Please correct the errors in the form.")
            for i, form in enumerate(formset):
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Passenger {i+1} - {field}: {error}")
    else:
        # Initialize formset with train parameter
        formset = PassengerFormSet(form_kwargs={'train': schedule.train})
    
    context = {
        'schedule': schedule,
        'from_station': from_station,
        'to_station': to_station,
        'price': price,
        'formset': formset,
        'existing_ticket': existing_ticket,
    }
    
    return render(request, 'mainApp/book_ticket.html', context)


def ticket_detail(request, pnr):
    ticket = get_object_or_404(Ticket, pnr=pnr)
    passengers = ticket.passengers.all()
    
    context = {
        'ticket': ticket,
        'passengers': passengers,
    }
    
    return render(request, 'mainApp/ticket_detail.html', context)

@check_login
def add_passengers(request, pnr):
    """Add more passengers to an existing ticket"""
    ticket = get_object_or_404(Ticket, pnr=pnr, booking_status='CONFIRMED')
    
    # Set session variables from the ticket
    request.session['schedule_id'] = ticket.schedule.id
    request.session['from_station_id'] = ticket.source_station.id if ticket.source_station else None
    request.session['to_station_id'] = ticket.destination_station.id if ticket.destination_station else None
    request.session['current_ticket_id'] = ticket.id
    
    return redirect('book_ticket')


def clear_ticket_session(request):
    """Clear current ticket from session"""
    if request.method == 'POST':
        request.session.pop('current_ticket_id', None)
        request.session.pop('schedule_id', None)
        request.session.pop('from_station_id', None)
        request.session.pop('to_station_id', None)
    return redirect('select_destinations')

