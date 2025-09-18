from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

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
    pnr_number = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    train_schedule = models.ForeignKey(TrainSchedule, on_delete=models.CASCADE)
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departure_tickets')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrival_tickets')
    booking_date = models.DateTimeField(auto_now_add=True)
    journey_date = models.DateField()
    booking_status = models.CharField(max_length=20, choices=[
        ('CONFIRMED', 'Confirmed'),
        ('WAITING', 'Waiting List'),
        ('RAC', 'RAC'),
        ('CANCELLED', 'Cancelled'),
    ], default='WAITING')
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"PNR: {self.pnr_number} - {self.user.username}"


class Passenger(models.Model):
    """Model for passengers in a ticket"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=10, choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other')
    ])
    seat_number = models.CharField(max_length=10, blank=True)
    berth_preference = models.CharField(max_length=15, choices=[
        ('LOWER', 'Lower'),
        ('MIDDLE', 'Middle'),
        ('UPPER', 'Upper'),
        ('SIDE_LOWER', 'Side Lower'),
        ('SIDE_UPPER', 'Side Upper'),
        ('NO_PREFERENCE', 'No Preference'),
    ], default='NO_PREFERENCE')
    current_status = models.CharField(max_length=20, choices=[
        ('CONFIRMED', 'Confirmed'),
        ('WAITING', 'Waiting List'),
        ('RAC', 'RAC'),
        ('CANCELLED', 'Cancelled'),
    ], default='WAITING')
    
    class Meta:
        ordering = ['ticket', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.ticket.pnr_number}"


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
