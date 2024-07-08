from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, DateInput
from django import forms
from .models import Record


# Register/create a new user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Create a record
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['purchase_date', 'product_name', 'serial_number', 'revision', 'customer_first_name', 'customer_last_name',
                  'address_street', 'address_building', 'address_apartment', 'address_city', 'address_postal_code', 'address_country',
                  'phone_number', 'email', 'auction_name', 'additional_info', 'gps_latitude', 'gps_longitude']
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'}),
        }


# Update a record
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['purchase_date', 'product_name', 'serial_number', 'revision', 'customer_first_name', 'customer_last_name',
                  'address_street', 'address_building', 'address_apartment', 'address_city', 'address_postal_code', 'address_country',
                  'phone_number', 'email', 'auction_name', 'additional_info', 'gps_latitude', 'gps_longitude']
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'}),
        }