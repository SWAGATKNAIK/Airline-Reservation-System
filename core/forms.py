from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

# Customer Signup Form
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.IS_CUSTOMER
        if commit:
            user.save()
        return user

# Login Form
class LoginForm(AuthenticationForm):
    # Standard Django AuthenticationForm is sufficient, 
    # but we can customize widgets if needed here.
    pass


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'aircraft', 'origin', 'destination', 
                  'departure_time', 'arrival_time', 'base_price']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'aircraft': forms.Select(attrs={'class': 'form-control'}),
        }

class AircraftForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ['code', 'name', 'total_economy_seats', 'total_business_seats']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B737'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Boeing 737 Max'}),
            'total_economy_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_business_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.IS_STAFF  # Force role to Staff
        user.is_staff = True # Django's internal flag for admin site access (optional, but good practice)
        if commit:
            user.save()
        return user

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PassengerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.IS_CUSTOMER  # Force role to Customer
        if commit:
            user.save()
        return user

class PassengerEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FlightSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From (City/Airport)'})
    )
    destination = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To (City/Airport)'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


class FlightStatusForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['status', 'gate']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'gate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A1, B3'}),
        }