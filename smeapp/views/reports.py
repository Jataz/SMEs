import requests
from django.http import JsonResponse
from collections import Counter
from django.conf import settings

# 1. Demographic Report API
def demographic_report_api(request):
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

        provinces = [sme['province']['province_name'] for sme in sme_data if sme.get('province')]
        province_counts = Counter(provinces)

        total_smes = len(provinces)
        percentages = {}
        if total_smes > 0:
            percentages = {province: round((count / total_smes) * 100, 2) for province, count in province_counts.items()}
        else:
            percentages = {province: 0 for province in province_counts.keys()}

        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(province_counts.values())

        # Return counts alongside other data
        return JsonResponse({'labels': labels, 'data': data, 'counts': counts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 2. Business Size Report API
def business_size_report_api(request):
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
        counts = list(size_of_business_counts.values())

        context = {
            'labels': labels,
            'data': data,
            'counts': counts
        }

        return JsonResponse(context)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 3. Financial Performance Report API
def financial_performance_report_api(request):
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

        sectors = [sme['sector']['name'] for sme in sme_data if sme.get('sector')]
        sector_revenue = Counter()

        for sme in sme_data:
            if sme.get('sector') and sme.get('annual_revenue'):
                sector_revenue[sme['sector']['name']] += float(sme['annual_revenue'])

        total_revenue = sum(sector_revenue.values())
        percentages = {}
        if total_revenue > 0:
            percentages = {sector: round((revenue / total_revenue) * 100, 2) for sector, revenue in sector_revenue.items()}
        else:
            percentages = {sector: 0 for sector in sector_revenue.keys()}

        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(sector_revenue.values())

        return JsonResponse({'labels': labels, 'data': data, 'counts': counts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 4. Export Report API
def export_report_api(request):
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

        export_status = [sme['export'] for sme in sme_data if sme.get('export')]
        export_counts = Counter(export_status)

        total_smes = len(export_status)
        percentages = {}
        if total_smes > 0:
            percentages = {status: round((count / total_smes) * 100, 2) for status, count in export_counts.items()}
        else:
            percentages = {status: 0 for status in export_counts.keys()}

        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(export_counts.values())

        return JsonResponse({'labels': labels, 'data': data, 'counts': counts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 5. Training and Education Report API
def training_education_report_api(request):
    try:
        # Get the session ID from cookies
        session_id = request.COOKIES.get('sessionid')

        # Send a GET request to the SME API endpoint
        response = requests.get(
            f'{settings.API_BASE_URL}/api/v1/smes/',
            cookies={'sessionid': session_id} if session_id else {}
        )

        # Process the response
        if response.status_code == 200:
            sme_data = response.json()
        else:
            # Handle non-200 responses gracefully
            sme_data = []

        # Extract the education levels from the response data
        education_levels = [sme.get('education') for sme in sme_data if sme.get('education')]

        # Count the occurrences of each education level
        education_counts = Counter(education_levels)

        # Calculate the total number of SMEs
        total_smes = len(education_levels)

        # Calculate percentages for each education level
        percentages = {}
        if total_smes > 0:
            percentages = {level: round((count / total_smes) * 100, 2) for level, count in education_counts.items()}
        else:
            percentages = {level: 0 for level in education_counts.keys()}

        # Prepare data for Chart.js
        labels = list(percentages.keys())  # Unique education levels
        data = list(percentages.values())  # Corresponding percentages
        counts = list(education_counts.values())  # Corresponding counts

        # Return the data as a JSON response
        return JsonResponse({'labels': labels, 'data': data,'counts':counts})

    except requests.exceptions.RequestException as req_err:
        # Handle request-related errors (e.g., network issues)
        return JsonResponse({'error': 'Failed to connect to the API', 'details': str(req_err)}, status=500)

    except Exception as e:
        # Catch any other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)


# 6. Gender Report API
def gender_api(request):
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
        counts = list(sex_counts.values())

        context = {
            'labels': labels,
            'data': data,
            'counts': counts
        }

        return JsonResponse(context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 7. Age Report API
def age_api(request):
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

        age_ranges = {
            "18-25": [18, 25],
            "26-35": [26, 35],
            "36-45": [36, 45],
            "46-55": [46, 55],
            "56+": [56, 100],
        }

        age_data = {key: 0 for key in age_ranges.keys()}
        for sme in sme_data:
            if 'age' in sme and sme['age'].isdigit():
                age = int(sme['age'])
                for key, value in age_ranges.items():
                    if value[0] <= age <= value[1]:
                        age_data[key] += 1

        labels = list(age_data.keys())
        data = list(age_data.values())

        return JsonResponse({'labels': labels, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
