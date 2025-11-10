from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import secrets
import string

# Create your models here.

class Station(models.Model):
    """Model for railway stations"""
    code = models.CharField(max_length=10, unique=True)  # e.g., 'MUM', 'DEL'
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Train(models.Model):
    """Model for trains"""
    train_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20, choices=[
        ('EXPRESS', 'Express'),
        ('SUPERFAST', 'Superfast'),
        ('PASSENGER', 'Passenger'),
        ('RAJDHANI', 'Rajdhani'),
        ('SHATABDI', 'Shatabdi'),
        ('DURONTO', 'Duronto'),
    ], default='EXPRESS')
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['train_number']
        constraints = [
            models.CheckConstraint(
                check=models.Q(available_seats__lte=models.F('total_seats')),
                name='available_seats_not_exceed_total'
            )
        ]
    
    @property
    def total_seats_calculated(self):
        """Calculate total seats from all coaches"""
        return sum(coach.total_seats for coach in self.coaches.all())
    
    def __str__(self):
        return f"{self.train_number} - {self.name}"


class TrainRoute(models.Model):
    """Model for train routes with intermediate stations"""
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    sequence_number = models.IntegerField()  # Order of stations in route
    arrival_time = models.TimeField(null=True, blank=True)  # Null for source station
    departure_time = models.TimeField(null=True, blank=True)  # Null for destination station
    distance_from_source = models.IntegerField(validators=[MinValueValidator(0)])  # km
    platform_number = models.CharField(max_length=5, blank=True)
    
    class Meta:
        ordering = ['train', 'sequence_number']
        unique_together = ['train', 'sequence_number']
        constraints = [
            models.CheckConstraint(
                check=models.Q(distance_from_source__gte=0),
                name='distance_non_negative'
            )
        ]
    
    def __str__(self):
        return f"{self.train.train_number} - {self.station.code} (Seq: {self.sequence_number})"


class TrainSchedule(models.Model):
    """Model for daily train schedules"""
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    journey_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('DELAYED', 'Delayed'),
        ('CANCELLED', 'Cancelled'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
    ], default='SCHEDULED')
    delay_minutes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['train', 'journey_date']
        ordering = ['journey_date', 'train']
    
    def __str__(self):
        return f"{self.train.train_number} - {self.journey_date} ({self.status})"


class Ticket(models.Model):
    """Model for ticket bookings"""
    BOOKING_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    schedule = models.ForeignKey('TrainSchedule', on_delete=models.PROTECT, related_name='tickets')
    passenger_name = models.CharField(max_length=100, default='Passenger')
    email = models.EmailField(blank=True)
    seat_class = models.CharField(max_length=20, choices=[
        ('GENERAL', 'General'),
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('FIRST_CLASS', 'First Class'),
    ], default='GENERAL')
    source_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='tickets_from', null=True)
    destination_station = models.ForeignKey('Station', on_delete=models.PROTECT, related_name='tickets_to', null=True)
    pnr = models.CharField(max_length=14, unique=True, editable=False)
    booked_at = models.DateTimeField(default=timezone.now)
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='CONFIRMED')
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = _generate_unique_pnr()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pnr} - {self.passenger_name}"

def _generate_unique_pnr():
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(10):
        pnr = ''.join(secrets.choice(alphabet) for _ in range(10))
        if not Ticket.objects.filter(pnr=pnr).exists():
            return pnr
    # Fallback with longer PNR if collisions (very unlikely)
    return ''.join(secrets.choice(alphabet) for _ in range(14))


class Coach(models.Model):
    COACH_TYPE_CHOICES = [
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('FIRST_CLASS', 'First Class'),
    ]
    
    train = models.ForeignKey('Train', on_delete=models.CASCADE, related_name='coaches')
    coach_number = models.CharField(max_length=10)
    coach_type = models.CharField(max_length=20, choices=COACH_TYPE_CHOICES)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    
    # Berth tracking
    total_lower = models.IntegerField(default=0)
    available_lower = models.IntegerField(default=0)
    total_middle = models.IntegerField(default=0)
    available_middle = models.IntegerField(default=0)
    total_upper = models.IntegerField(default=0)
    available_upper = models.IntegerField(default=0)
    total_side_lower = models.IntegerField(default=0)
    available_side_lower = models.IntegerField(default=0)
    total_side_upper = models.IntegerField(default=0)
    available_side_upper = models.IntegerField(default=0)

    class Meta:
        ordering = ['train', 'coach_number']
        unique_together = ['train', 'coach_number']

    def __str__(self):
        return f"{self.train.train_number} - {self.coach_number} ({self.coach_type})"
    
    def get_available_berth_type(self, preference=None):
        """Get available berth type based on preference or availability"""
        berth_availability = {
            'LOWER': self.available_lower,
            'MIDDLE': self.available_middle,
            'UPPER': self.available_upper,
            'SIDE_LOWER': self.available_side_lower,
            'SIDE_UPPER': self.available_side_upper,
        }
        
        # If preference is given and available, return it
        if preference and berth_availability.get(preference, 0) > 0:
            return preference
        
        # Otherwise, return first available berth type
        for berth_type, count in berth_availability.items():
            if count > 0:
                return berth_type
        
        return None
    
    def allocate_berth(self, berth_type):
        """Decrease available berth count when allocated"""
        if berth_type == 'LOWER':
            self.available_lower -= 1
        elif berth_type == 'MIDDLE':
            self.available_middle -= 1
        elif berth_type == 'UPPER':
            self.available_upper -= 1
        elif berth_type == 'SIDE_LOWER':
            self.available_side_lower -= 1
        elif berth_type == 'SIDE_UPPER':
            self.available_side_upper -= 1
        self.available_seats -= 1
        self.save()


class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    SEAT_CLASS_CHOICES = [
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('FIRST_CLASS', 'First Class'),
    ]
    
    BERTH_TYPE_CHOICES = [
        ('LOWER', 'Lower Berth'),
        ('MIDDLE', 'Middle Berth'),
        ('UPPER', 'Upper Berth'),
        ('SIDE_LOWER', 'Side Lower Berth'),
        ('SIDE_UPPER', 'Side Upper Berth'),
    ]
    
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('WAITING', 'Waiting List'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS_CHOICES, default='SLEEPER')
    coach = models.ForeignKey('Coach', on_delete=models.SET_NULL, null=True, blank=True)
    seat_number = models.CharField(max_length=10, blank=True)
    berth_type = models.CharField(max_length=15, choices=BERTH_TYPE_CHOICES, blank=True, null=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    booking_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['ticket', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['coach', 'seat_number'],
                name='unique_seat_per_coach',
                condition=~models.Q(seat_number='')
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.ticket.pnr}"

    def save(self, *args, **kwargs):
        # Ensure ticket is set before processing seat assignment
        if not self.seat_number and self.coach and self.ticket:
            berth_pref = kwargs.pop('berth_preference', None)
            
            # Determine berth type based on coach type and availability
            if self.coach.coach_type in ['SLEEPER', 'AC_3_TIER']:
                # 3-tier berth pattern
                berth_type = self.coach.get_available_berth_type(berth_pref)
                
                if berth_type:
                    # Get the next seat number for this berth type
                    seat_number = self._get_next_seat_for_berth(berth_type)
                    
                    if seat_number:
                        self.seat_number = str(seat_number)
                        self.berth_type = berth_type
                        self.coach.allocate_berth(berth_type)
                        self.current_status = 'CONFIRMED'
                    else:
                        self.current_status = 'WAITING'
                else:
                    self.current_status = 'WAITING'
                
            elif self.coach.coach_type == 'AC_2_TIER':
                # 2-tier berth pattern (no middle berth)
                berth_type = self.coach.get_available_berth_type(berth_pref)
                
                if berth_type:
                    seat_number = self._get_next_seat_for_berth(berth_type)
                    
                    if seat_number:
                        self.seat_number = str(seat_number)
                        self.berth_type = berth_type
                        self.coach.allocate_berth(berth_type)
                        self.current_status = 'CONFIRMED'
                    else:
                        self.current_status = 'WAITING'
                else:
                    self.current_status = 'WAITING'
                
            elif self.coach.coach_type == 'AC_1_TIER':
                # 1-tier (only lower and upper)
                berth_type = self.coach.get_available_berth_type(berth_pref)
                
                if berth_type:
                    seat_number = self._get_next_seat_for_berth(berth_type)
                    
                    if seat_number:
                        self.seat_number = str(seat_number)
                        self.berth_type = berth_type
                        self.coach.allocate_berth(berth_type)
                        self.current_status = 'CONFIRMED'
                    else:
                        self.current_status = 'WAITING'
                else:
                    self.current_status = 'WAITING'
    
        super().save(*args, **kwargs)

    def _get_next_seat_for_berth(self, berth_type):
        """Get the next available seat number for a specific berth type"""
        # Get all occupied seats for this coach on this specific schedule
        occupied_seats = set(Passenger.objects.filter(
            coach=self.coach,
            ticket__schedule=self.ticket.schedule,
            current_status__in=['CONFIRMED', 'WAITING']
        ).exclude(
            id=self.id  # Exclude current passenger if updating
        ).values_list('seat_number', flat=True))
        
        if self.coach.coach_type in ['SLEEPER', 'AC_3_TIER']:
            # 72 seats: Main berths (1-63) + Side berths (64-72)
            if berth_type == 'LOWER':
                seats = [i for i in range(1, 64, 3)]
            elif berth_type == 'MIDDLE':
                seats = [i for i in range(2, 64, 3)]
            elif berth_type == 'UPPER':
                seats = [i for i in range(3, 64, 3)]
            elif berth_type == 'SIDE_LOWER':
                seats = [i for i in range(64, 73, 2)]
            elif berth_type == 'SIDE_UPPER':
                seats = [i for i in range(65, 73, 2)]
            else:
                return None
            
        elif self.coach.coach_type == 'AC_2_TIER':
            # 48 seats: Main berths (1-42) + Side berths (43-48)
            if berth_type == 'LOWER':
                seats = [i for i in range(1, 43, 2)]
            elif berth_type == 'UPPER':
                seats = [i for i in range(2, 43, 2)]
            elif berth_type == 'SIDE_LOWER':
                seats = [i for i in range(43, 49, 2)]
            elif berth_type == 'SIDE_UPPER':
                seats = [i for i in range(44, 49, 2)]
            else:
                return None
            
        elif self.coach.coach_type == 'AC_1_TIER':
            # 24 seats (all cabins)
            if berth_type == 'LOWER':
                seats = [i for i in range(1, 25, 2)]
            elif berth_type == 'UPPER':
                seats = [i for i in range(2, 25, 2)]
            else:
                return None
        else:
            return None
    
        # Find first available seat
        for seat in seats:
            if str(seat) not in occupied_seats:
                return seat
        
        return None
        

class Payment(models.Model):
    """Model for payment transactions"""
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=[
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('NET_BANKING', 'Net Banking'),
        ('UPI', 'UPI'),
        ('WALLET', 'Digital Wallet'),
    ])
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
        ('REFUNDED', 'Refunded'),
    ], default='PENDING')
    gateway_response = models.TextField(blank=True)  # Store payment gateway response
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"


class Fare(models.Model):
    """Model for fare structure between stations"""
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='fare_from')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='fare_to')
    distance = models.IntegerField(validators=[MinValueValidator(1)])  # Distance in km
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    reservation_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tatkal_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['train', 'source_station', 'destination_station']
    
    def total_fare(self):
        return self.base_fare + self.reservation_charge
    
    def tatkal_fare(self):
        return self.base_fare + self.reservation_charge + self.tatkal_charge
    
    def __str__(self):
        return f"{self.train.train_number}: {self.source_station.code} → {self.destination_station.code}"


class WaitingList(models.Model):
    """Model to track waiting list positions"""
    passenger = models.OneToOneField(Passenger, on_delete=models.CASCADE)
    waiting_list_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['booking_date']
    
    def __str__(self):
        return f"WL {self.waiting_list_number} - {self.passenger.name}"
