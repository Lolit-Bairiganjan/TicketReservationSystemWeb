from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time, timedelta
from mainApp.models import Station, Train, TrainRoute, TrainSchedule, Fare, Coach

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Clear existing data
        Coach.objects.all().delete()
        TrainSchedule.objects.all().delete()
        Fare.objects.all().delete()
        TrainRoute.objects.all().delete()
        Train.objects.all().delete()
        Station.objects.all().delete()
        
        # Create stations
        delhi = Station.objects.create(code='DEL', name='Delhi Junction', city='Delhi', state='Delhi')
        mumbai = Station.objects.create(code='MUM', name='Mumbai Central', city='Mumbai', state='Maharashtra')
        agra = Station.objects.create(code='AGR', name='Agra Cantt', city='Agra', state='Uttar Pradesh')
        jaipur = Station.objects.create(code='JP', name='Jaipur Junction', city='Jaipur', state='Rajasthan')
        kolkata = Station.objects.create(code='KOAA', name='Kolkata', city='Kolkata', state='West Bengal')
        chennai = Station.objects.create(code='MAS', name='Chennai Central', city='Chennai', state='Tamil Nadu')
        bangalore = Station.objects.create(code='SBC', name='Bangalore City', city='Bangalore', state='Karnataka')
        ahmedabad = Station.objects.create(code='ADI', name='Ahmedabad Junction', city='Ahmedabad', state='Gujarat')

        # Create trains with correct total_seats
        train1 = Train.objects.create(train_number='IC101', name='InterCity Express', train_type='EXPRESS', total_seats=832, available_seats=832)
        train2 = Train.objects.create(train_number='SH200', name='Shatabdi Express', train_type='SHATABDI', total_seats=576, available_seats=576)
        train3 = Train.objects.create(train_number='RAJ301', name='Rajdhani Express', train_type='RAJDHANI', total_seats=384, available_seats=384)
        train4 = Train.objects.create(train_number='DUR401', name='Duronto Express', train_type='DURONTO', total_seats=832, available_seats=832)
        train5 = Train.objects.create(train_number='GARIB501', name='Garib Rath', train_type='EXPRESS', total_seats=640, available_seats=640)

        # Create coaches with berth distribution
        # Sleeper coach: 72 seats = 18 lower + 18 middle + 18 upper + 9 side lower + 9 side upper
        for i in range(1, 9):
            Coach.objects.create(
                train=train1, 
                coach_number=f'S{i}', 
                coach_type='SLEEPER',
                total_seats=72,
                total_lower=18,
                total_middle=18,
                total_upper=18,
                total_side_lower=9,
                total_side_upper=9
            )
        
        # AC 3 Tier: 64 seats = 16 lower + 16 middle + 16 upper + 8 side lower + 8 side upper
        for i in range(1, 5):
            Coach.objects.create(
                train=train1, 
                coach_number=f'B{i}', 
                coach_type='AC_3_TIER',
                total_seats=64,
                total_lower=16,
                total_middle=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )

        # AC 3 Tier coaches for train2
        for i in range(1, 7):
            Coach.objects.create(
                train=train2, 
                coach_number=f'B{i}', 
                coach_type='AC_3_TIER',
                total_seats=64,
                total_lower=16,
                total_middle=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )
        
        # AC 2 Tier: 48 seats = 16 lower + 16 upper + 8 side lower + 8 side upper
        for i in range(1, 5):
            Coach.objects.create(
                train=train2, 
                coach_number=f'A{i}', 
                coach_type='AC_2_TIER',
                total_seats=48,
                total_lower=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )

        # AC 1 Tier: 24 seats = 12 lower + 12 upper
        for i in range(1, 3):
            Coach.objects.create(
                train=train3, 
                coach_number=f'H{i}', 
                coach_type='AC_1_TIER',
                total_seats=24,
                total_lower=12,
                total_upper=12
            )
        
        # AC 2 Tier for train3
        for i in range(1, 4):
            Coach.objects.create(
                train=train3, 
                coach_number=f'A{i}', 
                coach_type='AC_2_TIER',
                total_seats=48,
                total_lower=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )
        
        # AC 3 Tier for train3
        for i in range(1, 4):
            Coach.objects.create(
                train=train3, 
                coach_number=f'B{i}', 
                coach_type='AC_3_TIER',
                total_seats=64,
                total_lower=16,
                total_middle=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )

        # Sleeper coaches for train4
        for i in range(1, 9):
            Coach.objects.create(
                train=train4, 
                coach_number=f'S{i}', 
                coach_type='SLEEPER',
                total_seats=72,
                total_lower=18,
                total_middle=18,
                total_upper=18,
                total_side_lower=9,
                total_side_upper=9
            )
        
        # AC 3 Tier for train4
        for i in range(1, 5):
            Coach.objects.create(
                train=train4, 
                coach_number=f'B{i}', 
                coach_type='AC_3_TIER',
                total_seats=64,
                total_lower=16,
                total_middle=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )

        # AC 3 Tier for train5
        for i in range(1, 11):
            Coach.objects.create(
                train=train5, 
                coach_number=f'G{i}', 
                coach_type='AC_3_TIER',
                total_seats=64,
                total_lower=16,
                total_middle=16,
                total_upper=16,
                total_side_lower=8,
                total_side_upper=8
            )

        # Create routes
        TrainRoute.objects.create(train=train1, station=delhi, sequence_number=1, departure_time=time(9, 0), arrival_time=None, distance_from_source=0, platform_number='1')
        TrainRoute.objects.create(train=train1, station=agra, sequence_number=2, arrival_time=time(11, 0), departure_time=time(11, 5), distance_from_source=200, platform_number='2')
        TrainRoute.objects.create(train=train1, station=jaipur, sequence_number=3, arrival_time=time(13, 0), departure_time=None, distance_from_source=400, platform_number='3')

        TrainRoute.objects.create(train=train2, station=delhi, sequence_number=1, departure_time=time(6, 0), arrival_time=None, distance_from_source=0, platform_number='4')
        TrainRoute.objects.create(train=train2, station=mumbai, sequence_number=2, arrival_time=time(18, 0), departure_time=None, distance_from_source=1400, platform_number='5')

        TrainRoute.objects.create(train=train3, station=delhi, sequence_number=1, departure_time=time(16, 0), arrival_time=None, distance_from_source=0, platform_number='6')
        TrainRoute.objects.create(train=train3, station=kolkata, sequence_number=2, arrival_time=time(10, 0), departure_time=None, distance_from_source=1500, platform_number='7')

        TrainRoute.objects.create(train=train4, station=mumbai, sequence_number=1, departure_time=time(20, 0), arrival_time=None, distance_from_source=0, platform_number='8')
        TrainRoute.objects.create(train=train4, station=chennai, sequence_number=2, arrival_time=time(8, 0), departure_time=None, distance_from_source=1300, platform_number='9')

        TrainRoute.objects.create(train=train5, station=bangalore, sequence_number=1, departure_time=time(14, 0), arrival_time=None, distance_from_source=0, platform_number='10')
        TrainRoute.objects.create(train=train5, station=ahmedabad, sequence_number=2, arrival_time=time(6, 0), departure_time=None, distance_from_source=1200, platform_number='11')

        # Create schedules
        base_date = timezone.now().date()
        for train in [train1, train2, train3, train4, train5]:
            for i in range(7):
                journey_date = base_date + timedelta(days=i)
                TrainSchedule.objects.create(
                    train=train,
                    journey_date=journey_date,
                    status='SCHEDULED',
                    base_fare=500 + (i * 50)
                )

        # Create fares
        Fare.objects.create(train=train1, source_station=delhi, destination_station=agra, distance=200, base_fare=500, reservation_charge=20, tatkal_charge=50)
        Fare.objects.create(train=train1, source_station=agra, destination_station=jaipur, distance=200, base_fare=300, reservation_charge=15, tatkal_charge=30)
        Fare.objects.create(train=train1, source_station=delhi, destination_station=jaipur, distance=400, base_fare=750, reservation_charge=25, tatkal_charge=75)
        Fare.objects.create(train=train2, source_station=delhi, destination_station=mumbai, distance=1400, base_fare=2000, reservation_charge=50, tatkal_charge=100)
        Fare.objects.create(train=train3, source_station=delhi, destination_station=kolkata, distance=1500, base_fare=2200, reservation_charge=60, tatkal_charge=120)
        Fare.objects.create(train=train4, source_station=mumbai, destination_station=chennai, distance=1300, base_fare=1800, reservation_charge=45, tatkal_charge=90)
        Fare.objects.create(train=train5, source_station=bangalore, destination_station=ahmedabad, distance=1200, base_fare=1600, reservation_charge=40, tatkal_charge=80)

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Station.objects.count()} stations'))
        self.stdout.write(self.style.SUCCESS(f'Created {Train.objects.count()} trains'))
        self.stdout.write(self.style.SUCCESS(f'Created {Coach.objects.count()} coaches'))
        self.stdout.write(self.style.SUCCESS(f'Created {TrainSchedule.objects.count()} schedules'))