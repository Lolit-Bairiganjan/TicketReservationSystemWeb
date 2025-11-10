from django import forms
from django.utils import timezone
from django.forms import formset_factory
from datetime import timedelta
from .models import Train, Station, Passenger, Coach

class SearchForm(forms.Form):
    train = forms.ModelChoiceField(
        queryset=Train.objects.all(),
        empty_label="Select Train",
        label="Train",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    from_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        empty_label="Select Departure Station",
        label="From",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        empty_label="Select Arrival Station",
        label="To",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    journey_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Journey Date",
        initial=timezone.now().date()
    )

    def clean(self):
        cleaned_data = super().clean()
        from_station = cleaned_data.get('from_station')
        to_station = cleaned_data.get('to_station')
        
        if from_station and to_station and from_station == to_station:
            raise forms.ValidationError("Departure and arrival stations cannot be the same.")
        
        return cleaned_data


class BookingForm(forms.Form):
    pass

class PassengerForm(forms.ModelForm):
    berth_preference = forms.ChoiceField(
        choices=[('', 'No Preference')] + Passenger.BERTH_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Berth Preference'
    )
    
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender', 'seat_class', 'coach', 'berth_preference', 'seat_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'seat_class': forms.Select(attrs={'class': 'form-control'}),
            'coach': forms.Select(attrs={'class': 'form-control'}),
            'seat_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for auto-assign'}),
        }

    def __init__(self, *args, **kwargs):
        train = kwargs.pop('train', None)
        super().__init__(*args, **kwargs)
        
        if train:
            # Filter coaches by train
            self.fields['coach'].queryset = Coach.objects.filter(train=train)
            
            # Add data attribute to map seat class to coach types
            self.fields['coach'].widget.attrs['data-train-id'] = train.id
            
        self.fields['coach'].required = False
        self.fields['seat_number'].required = False

    def clean(self):
        cleaned_data = super().clean()
        seat_class = cleaned_data.get('seat_class')
        coach = cleaned_data.get('coach')
        seat_number = cleaned_data.get('seat_number')
        
        # Validate coach matches seat class
        if coach and seat_class:
            # Map seat class to coach types
            seat_class_to_coach_type = {
                'SLEEPER': 'SLEEPER',
                'AC_3_TIER': 'AC_3_TIER',
                'AC_2_TIER': 'AC_2_TIER',
                'AC_1_TIER': 'AC_1_TIER',
                'FIRST_CLASS': 'FIRST_CLASS',
            }
            
            expected_coach_type = seat_class_to_coach_type.get(seat_class)
            if coach.coach_type != expected_coach_type:
                raise forms.ValidationError(f"Selected coach {coach.coach_number} does not match seat class {seat_class}.")
        
        # Validate seat not already booked
        if coach and seat_number:
            if Passenger.objects.filter(coach=coach, seat_number=seat_number).exists():
                raise forms.ValidationError(f"Seat {seat_number} in coach {coach.coach_number} is already booked.")
        
        return cleaned_data


# Formset for multiple passengers (up to 6)
PassengerFormSet = formset_factory(PassengerForm, extra=1, max_num=6, can_delete=False)

from django import forms
from .models import Station, Train, Coach, Passenger

class DestinationSelectionForm(forms.Form):
    train = forms.ModelChoiceField(
        queryset=Train.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    journey_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    from_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    to_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )


class PassengerBookingForm(forms.Form):
    SEAT_CLASS_CHOICES = [
        ('', 'Select Class'),
        ('GENERAL', 'General'),
        ('SLEEPER', 'Sleeper'),
        ('AC_3_TIER', 'AC 3 Tier'),
        ('AC_2_TIER', 'AC 2 Tier'),
        ('AC_1_TIER', 'AC 1 Tier'),
        ('FIRST_CLASS', 'First Class'),
    ]
    
    BERTH_CHOICES = [
        ('', 'No Preference'),
        ('LOWER', 'Lower Berth'),
        ('MIDDLE', 'Middle Berth'),
        ('UPPER', 'Upper Berth'),
        ('SIDE_LOWER', 'Side Lower'),
        ('SIDE_UPPER', 'Side Upper'),
    ]
    
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter full name',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter age',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    seat_class = forms.ChoiceField(
        choices=SEAT_CLASS_CHOICES,
        widget=forms.Select(attrs={
            'id': 'seat_class',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200',
            'onchange': 'updateCoaches()'
        })
    )
    
    coach = forms.ChoiceField(
        choices=[('', 'Select Coach')],
        required=False,
        widget=forms.Select(attrs={
            'id': 'coach',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    berth_preference = forms.ChoiceField(
        choices=BERTH_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    mobile = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '10-digit mobile number',
            'pattern': '[0-9]{10}',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )


class PassengerForm(forms.ModelForm):
    berth_preference = forms.ChoiceField(
        choices=[('', 'No Preference')] + Passenger.BERTH_CHOICES,  # FIXED: Changed from BERTH_TYPE_CHOICES to BERTH_CHOICES
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )
    
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender', 'seat_class', 'berth_preference']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter full name',
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Enter age',
                'min': '1',
                'max': '120',
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
            }),
            'seat_class': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        
        # Validate age range
        if age and (age < 1 or age > 120):
            raise forms.ValidationError('Age must be between 1 and 120')
        
        return cleaned_data


# Create a formset for multiple passengers
from django.forms import formset_factory
PassengerFormSet = formset_factory(PassengerForm, extra=1, max_num=6)


class PNRSearchForm(forms.Form):
    pnr = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 10-digit PNR',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200',
            'pattern': '[A-Z0-9]{10}',
            'style': 'text-transform: uppercase;'
        })
    )
    
    def clean_pnr(self):
        pnr = self.cleaned_data.get('pnr')
        if pnr:
            return pnr.upper()
        return pnr


class SearchForm(forms.Form):
    """Simple search form for trains"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by train number or name',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition duration-200'
        })
    )