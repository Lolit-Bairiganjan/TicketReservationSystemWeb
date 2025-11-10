from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import secrets
import string
from decimal import Decimal

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
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # ADD THIS
    
    class Meta:
        unique_together = ['train', 'journey_date']
        ordering = ['journey_date', 'train']
    
    def __str__(self):
        return f"{self.train.train_number} - {self.journey_date} ({self.status})"
    
    def get_total_seats(self):
        """Get total seats from the train's coaches"""
        return self.train.coaches.aggregate(
            total=models.Sum('total_seats')
        )['total'] or 0
    
    def get_available_seats(self):
        """Get available seats by calculating booked seats for this specific schedule"""
        # Get all passengers for this schedule across all tickets
        booked_count = Passenger.objects.filter(
            ticket__schedule=self,
            current_status__in=['CONFIRMED', 'RAC', 'WAITING']
        ).count()
        
        return self.get_total_seats() - booked_count
    
    def get_booked_seats(self):
        """Get total booked seats for this schedule"""
        return Passenger.objects.filter(
            ticket__schedule=self,
            current_status__in=['CONFIRMED', 'RAC', 'WAITING']
        ).count()

class Ticket(models.Model):
    """Model for train tickets"""
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('WAITING', 'Waiting List'),
    ]
    
    pnr = models.CharField(max_length=10, unique=True, editable=False)
    schedule = models.ForeignKey(TrainSchedule, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    seat_class = models.CharField(max_length=20)
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source_tickets', null=True, blank=True)
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_tickets', null=True, blank=True)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    booking_date = models.DateTimeField(auto_now_add=True)  # ADD auto_now_add=True
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        """Generate PNR if not exists"""
        if not self.pnr:
            import random
            import string
            # Generate a 10-character alphanumeric PNR
            self.pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # Ensure uniqueness
            while Ticket.objects.filter(pnr=self.pnr).exists():
                self.pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"PNR: {self.pnr} - {self.passenger_name}"
    
    def get_total_fare(self):
        """Calculate total fare from all passengers"""
        return sum(passenger.get_fare() for passenger in self.passengers.all())
    
    def get_seat_classes(self):
        """Get all unique seat classes for this ticket"""
        classes = list(self.passengers.values_list('seat_class', flat=True).distinct())
        if classes:
            # Convert codes to display names
            display_names = {
                'GENERAL': 'General',
                'SLEEPER': 'Sleeper',
                'AC_3_TIER': 'AC 3-Tier',
                'AC_2_TIER': 'AC 2-Tier',
                'AC_1_TIER': 'AC 1-Tier',
                'FIRST_CLASS': 'First Class',
            }
            return ', '.join([display_names.get(c, c) for c in classes])
        return self.seat_class
    
    class Meta:
        ordering = ['-booking_date']

class Coach(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='coaches')
    coach_number = models.CharField(max_length=10)
    coach_type = models.CharField(max_length=20, choices=[
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('GENERAL', 'General'),
        ('FIRST_CLASS', 'First Class'),
    ])
    total_seats = models.IntegerField()
    
    # Berth distribution
    total_lower = models.IntegerField(default=0)
    total_middle = models.IntegerField(default=0)
    total_upper = models.IntegerField(default=0)
    total_side_lower = models.IntegerField(default=0)
    total_side_upper = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['train', 'coach_number']
    
    def __str__(self):
        return f"{self.train.train_number} - {self.coach_number} ({self.coach_type})"
    
    @property
    def available_seats(self):
        """Calculate available seats dynamically"""
        booked_count = self.passengers.filter(
            current_status__in=['CONFIRMED', 'RAC', 'WAITING']
        ).count()
        return self.total_seats - booked_count
    
    @property
    def available_lower(self):
        booked = self.passengers.filter(berth_type='LOWER', current_status='CONFIRMED').count()
        return self.total_lower - booked
    
    @property
    def available_middle(self):
        booked = self.passengers.filter(berth_type='MIDDLE', current_status='CONFIRMED').count()
        return self.total_middle - booked
    
    @property
    def available_upper(self):
        booked = self.passengers.filter(berth_type='UPPER', current_status='CONFIRMED').count()
        return self.total_upper - booked
    
    @property
    def available_side_lower(self):
        booked = self.passengers.filter(berth_type='SIDE_LOWER', current_status='CONFIRMED').count()
        return self.total_side_lower - booked
    
    @property
    def available_side_upper(self):
        booked = self.passengers.filter(berth_type='SIDE_UPPER', current_status='CONFIRMED').count()
        return self.total_side_upper - booked

class Passenger(models.Model):
    """Model for individual passengers"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BERTH_CHOICES = [
        ('LOWER', 'Lower'),
        ('MIDDLE', 'Middle'),
        ('UPPER', 'Upper'),
        ('SIDE_LOWER', 'Side Lower'),
        ('SIDE_UPPER', 'Side Upper'),
    ]
    
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('RAC', 'RAC'),
        ('WAITING', 'Waiting List'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seat_class = models.CharField(max_length=20, choices=[
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('GENERAL', 'General'),
        ('FIRST_CLASS', 'First Class'),
    ])
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this line
    coach = models.ForeignKey(
        'Coach', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='passengers'  # ADD THIS LINE
    )
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    berth_type = models.CharField(max_length=20, choices=BERTH_CHOICES, blank=True, null=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    
    def __str__(self):
        return f"{self.name} - {self.ticket.pnr}"
    
    def save(self, *args, **kwargs):
        """Auto-assign seat and berth when passenger is created"""
        berth_preference = kwargs.pop('berth_preference', None)
        
        if not self.seat_number and self.coach:
            # Get berth preference or auto-assign
            available_berths = []
            
            # Check berth availability based on preference
            if berth_preference == 'LOWER' and self.coach.available_lower > 0:
                self.berth_type = 'LOWER'
            elif berth_preference == 'MIDDLE' and self.coach.available_middle > 0:
                self.berth_type = 'MIDDLE'
            elif berth_preference == 'UPPER' and self.coach.available_upper > 0:
                self.berth_type = 'UPPER'
            elif berth_preference == 'SIDE_LOWER' and self.coach.available_side_lower > 0:
                self.berth_type = 'SIDE_LOWER'
            elif berth_preference == 'SIDE_UPPER' and self.coach.available_side_upper > 0:
                self.berth_type = 'SIDE_UPPER'
            else:
                # Auto-assign any available berth
                if self.coach.available_lower > 0:
                    self.berth_type = 'LOWER'
                elif self.coach.available_middle > 0:
                    self.berth_type = 'MIDDLE'
                elif self.coach.available_upper > 0:
                    self.berth_type = 'UPPER'
                elif self.coach.available_side_lower > 0:
                    self.berth_type = 'SIDE_LOWER'
                elif self.coach.available_side_upper > 0:
                    self.berth_type = 'SIDE_UPPER'
            
            # Generate seat number
            if self.berth_type:
                # Count existing seats of this berth type in this coach
                existing_count = Passenger.objects.filter(
                    coach=self.coach,
                    berth_type=self.berth_type,
                    current_status='CONFIRMED'
                ).count()
                
                # Generate seat number (e.g., "12L" for 12th Lower berth)
                berth_code = {
                    'LOWER': 'L',
                    'MIDDLE': 'M',
                    'UPPER': 'U',
                    'SIDE_LOWER': 'SL',
                    'SIDE_UPPER': 'SU',
                }
                self.seat_number = f"{existing_count + 1}{berth_code.get(self.berth_type, '')}"
        
        super().save(*args, **kwargs)
    
    def get_fare(self):
        """Calculate fare for this passenger based on seat class"""
        # If fare is already saved, return it
        if self.fare and self.fare > 0:
            return self.fare
            
        try:
            fare_obj = Fare.objects.get(
                train=self.ticket.schedule.train,
                source_station=self.ticket.source_station,
                destination_station=self.ticket.destination_station
            )
            base_fare = fare_obj.base_fare
        except Fare.DoesNotExist:
            base_fare = self.ticket.schedule.base_fare
        
        # Class-based fare multipliers (using Decimal)
        class_multipliers = {
            'GENERAL': Decimal('1.0'),
            'SLEEPER': Decimal('1.5'),
            'AC_3_TIER': Decimal('2.0'),
            'AC_2_TIER': Decimal('3.0'),
            'AC_1_TIER': Decimal('5.0'),
            'FIRST_CLASS': Decimal('6.0'),
        }
        
        return base_fare * class_multipliers.get(self.seat_class, Decimal('1.0'))

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
