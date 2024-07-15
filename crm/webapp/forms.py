from .models import Record
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, DateInput
from import_export.formats.base_formats import DEFAULT_FORMATS
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumbers import PhoneNumber
import json
import phonenumbers


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PhoneNumber):
            # Assuming obj is a string that contains a valid phone number
            parsed_number = phonenumbers.parse(str(obj), None)
            # Format the number with the international format that includes the country code
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return formatted_number
        return super().default(obj)
    

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
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(), required=False)
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
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(), required=False)
    class Meta:
        model = Record
        fields = ['purchase_date', 'product_name', 'serial_number', 'revision', 'customer_first_name', 'customer_last_name',
                  'address_street', 'address_building', 'address_apartment', 'address_city', 'address_postal_code', 'address_country',
                  'phone_number', 'email', 'auction_name', 'additional_info', 'gps_latitude', 'gps_longitude']
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'}),
        }


# Import data
class ImportDataForm(forms.Form):
    file_format = forms.ChoiceField(choices=[(i, f().get_title()) for i, f in enumerate(DEFAULT_FORMATS)])
    import_file = forms.FileField()


# Export data
class ExportDataForm(forms.Form):
    file_format = forms.ChoiceField(choices=[(i, f().get_title()) for i, f in enumerate(DEFAULT_FORMATS)])
    # Assuming you want to let users select columns to export, you might need a dynamic way to generate these choices based on the model fields.
    # For simplicity, here's a static example:
    columns = forms.MultipleChoiceField(choices=[(field.name, field.name) for field in Record._meta.fields], widget=forms.CheckboxSelectMultiple)