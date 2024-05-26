import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings

from ..models import CalculationScale,SizeValue
from django.http import JsonResponse
from collections import Counter


# Create your views here.
@login_required(login_url="/login")
def index(request):
    session_id = request.COOKIES.get('sessionid')
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        sme_data = response.json()
    else:
        sme_data = []
    
        # Initialize counters
    male_count = 0
    female_count = 0

    # Iterate through the sme_data and count males and females
    for sme in sme_data:
        if sme.get('sex') == 'Male':
            male_count += 1
        elif sme.get('sex') == 'Female':
            female_count += 1

    # Process the data to extract size_of_business
    size_of_business_list = [sme['calculation_scale'][0]['size_of_business']['size'] for sme in sme_data if sme.get('calculation_scale')]
    #print(size_of_business_list)
    # Count occurrences of each size_of_business
    micro_count = size_of_business_list.count('MICRO')
    small_count = size_of_business_list.count('SMALL')
    medium_count = size_of_business_list.count('MEDIUM')
    large_count = size_of_business_list.count('LARGE')

    total_count = len(size_of_business_list)

    total_percentage = round((total_count / total_count) * 100, 2) if total_count > 0 else 0
    micro_percentage = round((micro_count / total_count) * 100, 2) if total_count > 0 else 0
    small_percentage = round((small_count / total_count) * 100, 2) if total_count > 0 else 0
    medium_percentage = round((medium_count / total_count) * 100, 2) if total_count > 0 else 0
    large_percentage = round((large_count / total_count) * 100, 2) if total_count > 0 else 0

    context = {
        'micro_count': micro_count,
        'small_count': small_count,
        'medium_count': medium_count,
        'large_count': large_count,
        'sme_data':sme_data,
        'micro_percentage': micro_percentage,
        'small_percentage': small_percentage,
        'medium_percentage': medium_percentage,
        'large_percentage': large_percentage,
        'total_percentage':total_percentage,
        'total_count':total_count,
        'male_count': male_count,
        'female_count': female_count
    }

    return render(request, 'pages/dashboard/index.html', context)


@login_required(login_url="/login")
def sme_list(request):
    # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',       
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        smes = response.json() # Extract JSON data from the response
        return render(request, 'pages/smes/index.html',{'smes':smes})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch SMEs data'})
    
def size_of_business_data(request):
    session_id = request.COOKIES.get('sessionid')
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        sme_data = response.json()
    else:
        sme_data = []

    # Extract size_of_business from each calculation_scale
    size_of_businesses = [sme['calculation_scale'][0]['size_of_business']['size'] for sme in sme_data if sme.get('calculation_scale')]

    # Count the occurrences of each size_of_business
    size_of_business_counts = Counter(size_of_businesses)

    # Calculate the total number of SMEs
    total_smes = len(size_of_businesses)

    # Calculate percentages for each size category
    percentages = {size: (count / total_smes) * 100 for size, count in size_of_business_counts.items()}

    # Prepare data for Chart.js
    labels = list(percentages.keys())
    data = list(percentages.values())

    context = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(context)

def sex_data(request):
    session_id = request.COOKIES.get('sessionid')
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        sme_data = response.json()
    else:
        sme_data = []

    # Count the occurrences of each sex
    total_smes = len(sme_data)
    sex_counts = {'Male': 0, 'Female': 0}
    for sme in sme_data:
        sex = sme.get('sex')
        if sex in sex_counts:
            sex_counts[sex] += 1

    # Calculate percentages
    percentages = {}
    for sex, count in sex_counts.items():
        percentages[sex] = round((count / total_smes) * 100)

    # Prepare data for Chart.js
    labels = list(percentages.keys())
    data = list(percentages.values())

    context = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(context)
