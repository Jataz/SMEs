import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings

from ..models import SME, CalculationScale,SizeValue,Sector
from django.http import JsonResponse
from datetime import datetime
from collections import Counter
from django.db.models import Count, Avg, F
from django.views import View

def update_session(request):
    if request.user.is_authenticated:
        request.session['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse({"status": "session updated"})

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
    try:
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
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def size_of_business_data(request):
    try:
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
        size_of_businesses = [
            sme['calculation_scale'][0]['size_of_business']['size']
            for sme in sme_data if sme.get('calculation_scale')
        ]

        # Count the occurrences of each size_of_business
        size_of_business_counts = Counter(size_of_businesses)

        # Calculate the total number of SMEs
        total_smes = len(size_of_businesses)

        # Calculate percentages for each size category
        percentages = {}
        if total_smes > 0:
            percentages = {size: round((count / total_smes) * 100, 2) for size, count in size_of_business_counts.items()}
        else:
            percentages = {size: 0 for size in size_of_business_counts.keys()}

        # Prepare data for Chart.js
        labels = list(percentages.keys())
        data = list(percentages.values())

        context = {
            'labels': labels,
            'data': data,
        }

        return JsonResponse(context)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def sex_data(request):
    try:
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
        if total_smes > 0:
            for sex, count in sex_counts.items():
                percentages[sex] = round((count / total_smes) * 100)
        else:
            pass

        # Prepare data for Chart.js
        labels = list(percentages.keys())
        data = list(percentages.values())

        context = {
            'labels': labels,
            'data': data,
        }

        return JsonResponse(context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_sectors(request):
    """Return a list of sectors in JSON format."""
    if request.method == 'GET':
        sectors = list(Sector.objects.all().values('id', 'name'))
        return JsonResponse(sectors, safe=False)

def smes_by_age_range_filtered(province_id=None, district_id=None, ward_id=None):
    """Filter SMEs by location and return age range counts."""
    queryset = SME.objects.all()

    # Apply filters based on the provided location IDs
    if province_id:
        queryset = queryset.filter(province_id=province_id)
    if district_id:
        queryset = queryset.filter(district_id=district_id)
    if ward_id:
        queryset = queryset.filter(ward_id=ward_id)

    # Generate age range counts
    age_ranges = {
        "18-25": queryset.filter(age__gte=18, age__lte=25).count(),
        "26-35": queryset.filter(age__gte=26, age__lte=35).count(),
        "36-45": queryset.filter(age__gte=36, age__lte=45).count(),
        "46-55": queryset.filter(age__gte=46, age__lte=55).count(),
        "56+": queryset.filter(age__gte=56).count(),
    }
    return age_ranges

def age_range_report_filtered_view(request):
    province_id = request.GET.get('province_id')
    district_id = request.GET.get('district_id')
    ward_id = request.GET.get('ward_id')

    try:
        age_range_data = smes_by_age_range_filtered(province_id, district_id, ward_id)
        return JsonResponse({'age_range_report': age_range_data}, safe=False)
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=400)

class SMEReportsView(View):
    template_name = 'reports.html'

    def get_demographic_report(self):
        total_businesses = SME.objects.count()
        return SME.objects.values(province_name=F('province__province_name')).annotate(
            number_of_businesses=Count('id'),
            percentage=(Count('id') * 100.0 / total_businesses)
        ).order_by('-number_of_businesses')

    def get_business_size_report(self):
        total_businesses = SME.objects.count()
        return CalculationScale.objects.values(size_name=F('size_of_business__size')).annotate(
            number_of_businesses=Count('id'),
            percentage=(Count('id') * 100.0 / total_businesses)
        ).order_by('-number_of_businesses')

    def get_compliance_report(self):
        total_businesses = SME.objects.count()
        return SME.objects.values(compliance_status=F('tax')).annotate(
            number_of_businesses=Count('id'),
            percentage=(Count('id') * 100.0 / total_businesses)
        ).order_by('-number_of_businesses')

    def get_financial_performance_report(self):
        return SME.objects.values(sector_name=F('sector__name')).annotate(
            avg_annual_turnover=Avg('annual_revenue')
        ).order_by('-avg_annual_turnover')

    def get_export_report(self):
        total_businesses = SME.objects.count()
        return SME.objects.values(export_status=F('export')).annotate(
            number_of_businesses=Count('id'),
            percentage=(Count('id') * 100.0 / total_businesses)
        ).order_by('-number_of_businesses')

    def get_training_education_report(self):
        total_business_owners = SME.objects.count()
        return SME.objects.values(education_level=F('education')).annotate(
            number_of_business_owners=Count('id'),
            percentage=(Count('id') * 100.0 / total_business_owners)
        ).order_by('-number_of_business_owners')

    def get(self, request, *args, **kwargs):
        reports = {
            'demographic': self.get_demographic_report(),
            'business_size': self.get_business_size_report(),
            'compliance': self.get_compliance_report(),
            'financial_performance': self.get_financial_performance_report(),
            'export': self.get_export_report(),
            'training_education': self.get_training_education_report(),
        }
        return render(request, self.template_name, {'reports': reports})
