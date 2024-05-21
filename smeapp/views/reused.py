
@login_required(login_url="/login")
def index(request):
    
    # Query the database to get the count of each size_of_business category
    size_of_business_counts = Counter(CalculationScale.objects.values_list('size_of_business__size', flat=True))
        # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',       
        cookies={'sessionid': session_id} if session_id else {}
    )
    
        # Get serialized data from the response
    sme_data = response.json()

    # Get total count of CalculationScale instances
    total_count = CalculationScale.objects.count()

    # Get the primary keys for each size category
    micro_pk = SizeValue.objects.get(size='MICRO').pk
    small_pk = SizeValue.objects.get(size='SMALL').pk
    medium_pk = SizeValue.objects.get(size='MEDIUM').pk
    large_pk = SizeValue.objects.get(size='LARGE').pk

    # Count occurrences using primary keys
    micro_count = CalculationScale.objects.filter(size_of_business_id=micro_pk).count()
    small_count = CalculationScale.objects.filter(size_of_business_id=small_pk).count()
    medium_count = CalculationScale.objects.filter(size_of_business_id=medium_pk).count()
    large_count = CalculationScale.objects.filter(size_of_business_id=large_pk).count()

    # Calculate percentage counts
    micro_percentage = round((micro_count / total_count) * 100, 2) if total_count > 0 else 0
    small_percentage = round((small_count / total_count) * 100, 2) if total_count > 0 else 0
    medium_percentage = round((medium_count / total_count) * 100, 2) if total_count > 0 else 0
    large_percentage = round((large_count / total_count) * 100, 2) if total_count > 0 else 0

    context = {
        'micro_count': micro_count,
        'small_count': small_count,
        'medium_count': medium_count,
        'large_count': large_count,
        'micro_percentage': micro_percentage,
        'small_percentage': small_percentage,
        'medium_percentage': medium_percentage,
        'large_percentage': large_percentage,
        'sme_data':sme_data,
        'size_data': size_of_business_counts,
    }

    return render(request, 'pages/dashboard/index.html', context)
