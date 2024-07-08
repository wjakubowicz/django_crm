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