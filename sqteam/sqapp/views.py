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

from .models import Gate, Check, Trip


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


def app_view(request):
    trips, per = incorrect_trip()
    trips_count = Trip.objects.all().count()
    return render(request, 'app.html', {'trips': trips,
                                        'percentage': per,
                                        'trips_count': trips_count})

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


def total_load(request):
    from datetime import timedelta, datetime
    all_checks = Check.objects.all()
    print(all_checks)
    res = []
    if 'type' in request.GET:
        for c in all_checks:
            if c.gate.type == request.GET['type']:
                res.append(c)
    else:
        res.extend(all_checks)
    print(len(res))
    result = []
    if 'period' in request.GET:
        delt = None
        perid = request.GET['period']
        if perid == 'week':
            delt = timedelta(weeks=1)
        if perid == 'day':
            delt = timedelta(days=1)
        if perid == 'month':
            delt = timedelta(weeks=4)
        now = datetime.now()
        when = now - delt
        for c in res:
            if c.timestamp > when:
                result.append(c)
    else:
        result = res
    print(result)
    #metro = Check.objects.filter(gate__type == 'metro') # WHAT'S WRONG????

    return JsonResponse(len(result), safe=False)