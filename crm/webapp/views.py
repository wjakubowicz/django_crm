from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from .models import Record
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from geopy.exc import GeocoderServiceError
from geopy.geocoders import ArcGIS
import time
import folium


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
                messages.success(request, 'Zalogowałeś się!')
                return redirect('dashboard')
    
    context = {'form': form}
    return render(request, 'webapp/user_login.html', context=context)


# Dashboard
@login_required(login_url='user_login')
def dashboard(request):
    my_records = Record.objects.all()

    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html', context=context)


# Logout a user
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Wylogowałeś się!')
    return redirect('user_login')


# Create a record
@login_required(login_url='user_login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
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
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.info(request, 'Zmodyfikowałeś rekord!')
            return redirect('dashboard')
        
    context = {'form': form}
    return render(request, 'webapp/update_record.html', context=context)


# View a record
@login_required(login_url='user_login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record': all_records}
    return render(request, 'webapp/view_record.html', context=context)


# Delete a record
@login_required(login_url='user_login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.warning(request, 'Usunąłeś rekord!')
    return redirect('dashboard')


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

    messages.success(request, 'Współrzędne GPS zostały zaktualizowane!')
    return redirect('dashboard')


def view_map(request):
    tile_style = request.GET.get('tiles')  # Get the tile style from the request
    current_tiles = request.GET.get('tiles', 'default_value')  # Replace 'default_value' with your default tile style

    m = folium.Map(location=[52.114503, 19.423561], zoom_start=7, tiles=tile_style)  # Create a base map with the selected tile style

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
        folium.Marker(
            [record.gps_latitude, record.gps_longitude],
            popup=folium.Popup(info, max_width=450)
        ).add_to(m)

    map_html = m._repr_html_()
    context = {
        'map_html': map_html,
        'current_tiles': current_tiles,
    }
    return render(request, 'webapp/view_map.html', context)