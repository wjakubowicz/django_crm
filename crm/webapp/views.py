from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm, ImportDataForm, ExportDataForm
from .models import Record
from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from folium import plugins
from folium.plugins import Fullscreen
from geopy.exc import GeocoderServiceError
from geopy.geocoders import ArcGIS
from import_export import resources
from import_export.formats.base_formats import DEFAULT_FORMATS
from tablib import Dataset
from phonenumbers import PhoneNumber  # Import the PhoneNumber class
import phonenumbers
import folium
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, filename='crm_events.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger(__name__)


# Custom JSON Encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, PhoneNumber):
            # Assuming obj is a string that contains a valid phone number
            parsed_number = phonenumbers.parse(str(obj), None)
            # Format the number with the international format that includes the country code
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return formatted_number
        return super().default(obj)


# Home
def home(request):
    return render(request, 'webapp/index.html')


# Register a user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'New user registered: {request.user.username}')
            messages.success(request, 'Zarejestrowałeś się!')
            return redirect('user_login')
    
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)


# Login a user
def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                logger.info(f'User logged in: {request.user.username}')
                messages.success(request, 'Zalogowałeś się!')
                
                return redirect('dashboard')
    
    context = {'form': form}
    return render(request, 'webapp/user_login.html', context=context)


# Logout a user
def user_logout(request):
    logger.info(f"User logged out: {request.user.username}")
    auth.logout(request)
    messages.success(request, 'Wylogowałeś się!')
    return redirect('user_login')


# Dashboard
@login_required(login_url='user_login')
def dashboard(request):
    my_records = Record.objects.all()

    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html', context=context)


# Create a record
@login_required(login_url='user_login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            new_record = form.save()
            logger.info(f"User: {request.user.username} created a new record: {model_to_dict(new_record)}")
            messages.success(request, 'Utworzyłeś rekord!')
            return redirect('dashboard')
        
    context = {'form': form}
    return render(request, 'webapp/create_record.html', context=context)


# Update a record
@login_required(login_url='user_login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        original_record = model_to_dict(record)  # Capture original record
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            updated_record = model_to_dict(record)  # Capture updated record
            logger.info(f"User: {request.user.username} updated a record. Original: {json.dumps(original_record, cls=CustomJSONEncoder)}, Updated: {json.dumps(updated_record, cls=CustomJSONEncoder)}")
            messages.info(request, 'Zmodyfikowałeś rekord!')
            return redirect('dashboard')
        
    context = {'form': form}
    return render(request, 'webapp/update_record.html', context=context)


# Delete a record
@login_required(login_url='user_login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record_dict = model_to_dict(record)
    record.delete()
    logger.info(f"User: {request.user.username} deleted a record: {json.dumps(record_dict, cls=CustomJSONEncoder)}")
    messages.warning(request, 'Usunąłeś rekord!')
    return redirect('dashboard')


# View a record
@login_required(login_url='user_login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record': all_records}
    return render(request, 'webapp/view_record.html', context=context)


# Change theme
def change_theme(request):
    theme = request.GET.get('theme', 'default')
    request.session['theme'] = theme
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Update GPS coordinates
@login_required(login_url='user_login')
def update_record_coordinates(request):
    geolocator = ArcGIS()
    records = Record.objects.all()
    
    for record in records:
        address = f"{record.address_street} {record.address_building}/{record.address_apartment}, {record.address_postal_code} {record.address_city}, {record.address_country}"
        try:
            location = geolocator.geocode(address)
            if location:
                record.gps_latitude = location.latitude
                record.gps_longitude = location.longitude
                record.save()
        except GeocoderServiceError:
            time.sleep(1)  # delay for 1 second and skip this record or you could retry

    logger.info(f"User: {request.user.username} updated GPS coordinates for all records")
    messages.success(request, 'Współrzędne GPS zostały zaktualizowane!')
    return redirect('dashboard')


# View a map
@login_required(login_url='user_login')
def view_map(request):
    tile_style = request.GET.get('tiles', 'OpenStreetMap')  # Get the tile style from the request
    current_tiles = request.GET.get('tiles', 'default_value')  # Replace 'default_value' with your default tile style
    clusterize = request.GET.get('clusterize', 'off')  # Get the clusterize option from the request

    m = folium.Map(location=[52.114503, 19.423561], zoom_start=7, tiles=tile_style)  # Create a base map with the selected tile style centered on Poland
    Fullscreen().add_to(m)   

    if clusterize == 'on':
        marker_cluster = plugins.MarkerCluster().add_to(m)  # Create a MarkerCluster object

    records = Record.objects.all()  # Fetch records from the database

    # Iterate over records and add pins with detailed information
    for record in records:
        info = f"""
        <strong>ID:</strong> {record.id}<br>
        <strong>Data zakupu:</strong> {record.purchase_date}<br>
        <strong>Nazwa produktu:</strong> {record.product_name}<br>
        <strong>Numer seryjny:</strong> {record.serial_number}<br>
        <strong>Imię i nazwisko klienta:</strong> {record.customer_first_name} {record.customer_last_name}<br>
        <strong>Adres:</strong> {record.address_street} {record.address_building}/{record.address_apartment}, {record.address_postal_code} {record.address_city}, {record.address_country}<br>
        <strong>Numer telefonu:</strong> {record.phone_number}<br>
        <strong>Email:</strong> {record.email}<br>
        <strong>Nazwa aukcyjna:</strong> {record.auction_name}<br>
        <strong>Dodatkowe informacje:</strong> {record.additional_info}
        """
        marker = folium.Marker(
            [record.gps_latitude, record.gps_longitude],
            popup=folium.Popup(info, max_width=450)
        )
        if clusterize == 'on':
            marker.add_to(marker_cluster)  # Add the marker to the cluster
        else:
            marker.add_to(m)  # Add the marker directly to the map

    map_html = m._repr_html_()
    context = {
        'map_html': map_html,
        'current_tiles': current_tiles,
        'clusterize': clusterize,
    }
    return render(request, 'webapp/view_map.html', context)


# Import data
def import_data(request):
    if request.method == 'POST':
        form = ImportDataForm(request.POST, request.FILES)
        if form.is_valid():
            resource = resources.modelresource_factory(model=Record)()
            dataset = Dataset()
            new_records = request.FILES['import_file']  # Convert form.cleaned_data['file_format'] to an integer index
            file_format_index = int(form.cleaned_data['file_format'])  # Access the corresponding format class from DEFAULT_FORMATS
            file_format_class = DEFAULT_FORMATS[file_format_index]()  # Use the format's name when loading data into Tablib
            imported_data = dataset.load(new_records.read().decode('utf-8'), format=file_format_class.get_title())
            result = resource.import_data(dataset, dry_run=True)  # Test the data import
            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)  # Actually import now
                logger.info(f"User: {request.user.username} imported data from a file")
                messages.success(request, 'Dane zostały zaimportowane pomyślnie!')
            return redirect('dashboard')
    else:
        form = ImportDataForm()
    return render(request, 'webapp/import_data.html', {'form': form})


# Export data
@login_required(login_url='user_login')
def export_data(request):
    if request.method == 'POST':
        form = ExportDataForm(request.POST)
        if form.is_valid():
            resource = resources.modelresource_factory(model=Record)()
            dataset = resource.export()
            file_format = DEFAULT_FORMATS[int(form.cleaned_data['file_format'])]()
            response = HttpResponse(file_format.export_data(dataset), content_type=file_format.get_content_type())
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Generate timestamp as YYYY-MM-DD_HH-MM-SS
            response['Content-Disposition'] = 'attachment; filename="exported_data_{}.{}"'.format(timestamp, file_format.get_extension())
            logger.info(f"User: {request.user.username} exported data to a file")
            messages.success(request, 'Dane zostały wyeksportowane pomyślnie!')
            return response
    else:
        form = ExportDataForm()
    return render(request, 'webapp/export_data.html', {'form': form})