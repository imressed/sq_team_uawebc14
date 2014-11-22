from django.shortcuts import render, render_to_response, redirect
from django.shortcuts import HttpResponse, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_GET)
from django.http import JsonResponse

from .forms import UserCreationForm

from django.contrib import messages

from .models import Gate, Check, Trip, Card


def index(request):

    login_form = AuthenticationForm()
    signup_form = UserCreationForm()
    incorrect_trip()
    return render(request, 'index.html', {'login_form': login_form,
                                          'signup_form': signup_form})

@require_GET
def login_view(request):
    return render(request, 'index.html', {'show_login': True})

@require_GET
def signup_view(request):
    return render(request, 'index.html', {'show_signup': True})

@require_POST
def login_func(request):
    login_form = AuthenticationForm(data=request.POST)
    if login_form.is_valid():
        user = authenticate(username=login_form.cleaned_data.get('username'),
                            password=login_form.cleaned_data.get('password'))
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'next': '/app'})
    else:
        return JsonResponse({'success': False,
                             'errors': login_form.errors})

@require_GET
def logout_func(request):
    logout(request)
    return redirect('index')

@require_POST
def signup_func(request):
    signup_form = UserCreationForm(data=request.POST)
    if signup_form.is_valid():
        signup_form.save()
        messages.add_message(request, messages.INFO, 'Success sign up')
        return JsonResponse({'success': True, 'next': '/app',
                             'message': 'Success creation of new user'})
    return JsonResponse({'success': False,
                         'errors': signup_form.errors})



def trip_cards(request):
    print(request.GET['trip_number'])
    trips = Trip.objects.filter(card=Card.objects.get(request.POST['trip_number']))
    points = []
    for trip in trips:
        start = Gate.objects.get(point_id=trip.point_start)
        finish = Gate.objects.get(point_id=trip.point_finish)
        points.append({'x_start':start.coord_x,'y_start':start.coord_y,'x_finish':finish.coord_x,'y_finish':finish.coord_y})
    return JsonResponse({'trips':points})


def app_view(request):
    trips, per = incorrect_trip()
    cards = Card.objects.all()
    return render(request, 'app.html', {'trips': trips,
                                        'percentage': per,
                                        'cards': cards})

def incorrect_trip():
    trips = Trip.objects.all()
    bad_trips = []

    for trip in trips:
        check_in = Check.objects.get(type='in',trip=trip.id)
        check_out = Check.objects.get(type='out',trip=trip.id)
        if trip.point_start == check_in.gate and trip.point_finish == check_out.gate:
            print('good trip')
        else:
            bad_trips.append(trip)
    bad_trips_per = len(bad_trips)/len(trips)*100
    return bad_trips, bad_trips_per
