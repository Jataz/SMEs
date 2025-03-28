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
def ownership_api(request):
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

        # Count the occurrences of each ownership type
        total_smes = len(sme_data)
        ownership_counts = Counter()
        for sme in sme_data:
            ownership = sme.get('ownership')
            if ownership:
                ownership_counts[ownership] += 1

        # Calculate percentages
        percentages = {}
        if total_smes > 0:
            for ownership, count in ownership_counts.items():
                percentages[ownership] = round((count / total_smes) * 100, 2)

        # Prepare data for Chart.js
        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(ownership_counts.values())

        context = {
            'labels': labels,
            'data': data,
            'counts': counts
        }

        return JsonResponse(context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 7. Asset Performance Report API
def asset_performance_report_api(request):
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
            if sme.get('sector') and sme.get('asset_value'):
                sector_revenue[sme['sector']['name']] += float(sme['asset_value'])

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
 
#Business support report
def business_support_api(request):
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

        # Count the occurrences of each support service
        total_smes = len(sme_data)
        support_counts = Counter()
        for sme in sme_data:
            support_service = sme.get('support_service')
            if support_service:
                if isinstance(support_service, list):
                    for service in support_service:
                        support_counts[str(service)] += 1
                else:
                    support_counts[str(support_service)] += 1

        # Calculate percentages
        percentages = {}
        if total_smes > 0:
            for service, count in support_counts.items():
                percentages[service] = round((count / total_smes) * 100, 2)

        # Prepare data for Chart.js
        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(support_counts.values())

        context = {
            'labels': labels,
            'data': data,
            'counts': counts
        }

        return JsonResponse(context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#Number of Employees by Sector
def employees_by_sector_api(request):
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
        sector_employees = Counter()

        for sme in sme_data:
            if sme.get('sector') and sme.get('number_of_employees'):
                sector_employees[sme['sector']['name']] += int(sme['number_of_employees'])

        total_employees = sum(sector_employees.values())
        percentages = {}
        if total_employees > 0:
            percentages = {sector: round((employees / total_employees) * 100, 2) for sector, employees in sector_employees.items()}
        else:
            percentages = {sector: 0 for sector in sector_employees.keys()}

        labels = list(percentages.keys())
        data = list(percentages.values())
        counts = list(sector_employees.values())

        return JsonResponse({'labels': labels, 'data': data, 'counts': counts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)