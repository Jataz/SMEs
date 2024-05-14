from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import SME,Province,District,SizeValue,CalculationScale

from ..serializers import SMESerializer,ProvinceSerializer,DistrictSerializer


class ProvinceAPIView(APIView):
    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response({'provinces': serializer.data})

class DistrictAPIView(APIView):
    def get(self, request):
        province_id = request.GET.get('province_id')
        districts = District.objects.filter(province_id=province_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response({'districts': serializer.data})
class SMECreate(generics.CreateAPIView):
    queryset = SME.objects.all()
    serializer_class = SMESerializer

class SMEListView(APIView):
    def get(self, request):
        # Filter SMEs with associated calculation scales
        matched_smes = SME.objects.filter(calculation_scale__isnull=False)

        # Serialize SMEs along with related calculation scales and size values
        serializer = SMESerializer(matched_smes, many=True, context={'request': request})

        # Return serialized data
        return Response(serializer.data)
    
@csrf_exempt
def sme_record(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        
        # Retrieve form data
        company = form_data.get('company')
        contact_person = form_data.get('contact_person')
        phone_number = form_data.get('phone_number')
        email = form_data.get('email')
        address = form_data.get('address')
        sector = form_data.get('sector')
        type_of_business = form_data.get('type_of_business')
        product_service = form_data.get('product_service')
        province_id = form_data.get('province_id')
        district_id = form_data.get('district_id')
        number_of_employees = int(form_data.get('number_of_employees'))  # Convert to integer
        asset_value = form_data.get('asset_value')
        annual_revenue = form_data.get('annual_revenue')
        
        try:
            annual_revenue = int(form_data.get('annual_revenue'))
            asset_value = int(form_data.get('asset_value'))
        except ValueError:
            return JsonResponse({'error': 'Invalid value for annual revenue or asset value'}, status=400)

        
        # Validate form data
        if not all([company, contact_person, phone_number, email, address, sector, type_of_business, product_service,
                    province_id, district_id, number_of_employees, asset_value, annual_revenue]):
            return JsonResponse({'error': 'Please fill in all fields'}, status=400)
        
        # Start a database transaction
        with transaction.atomic():
            try:
                # Create SME record
                sme = create_sme_record(company, contact_person, phone_number, email, address, sector,
                                         type_of_business, product_service, province_id, district_id,
                                         number_of_employees, asset_value, annual_revenue)
                
                # Determine rating based on number_of_employees, annual_revenue, and asset_value
                size_of_employees = determine_size_of_employees(number_of_employees)
                size_of_annual_revenue = determine_size_of_annual_revenue(annual_revenue)
                size_of_asset_value = determine_size_of_asset_value(asset_value)
                rating = calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value)
                
                # Determine the size of the business based on rating
                size_of_business = determine_business_size(rating)
                
                # Create CalculationScale record
                create_calculation_scale(sme, size_of_employees, size_of_annual_revenue, size_of_asset_value,
                                         rating, size_of_business)
                
                return JsonResponse({'success': 'SME added successfully'}, status=201)
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def create_sme_record(company, contact_person, phone_number, email, address, sector,
                      type_of_business, product_service, province_id, district_id,
                      number_of_employees, asset_value, annual_revenue):
    """Create an SME record."""

    sme = SME.objects.create(
        company=company,
        contact_person=contact_person,
        phone_number=phone_number,
        email=email,
        address=address,
        sector=sector,
        type_of_business=type_of_business,
        product_service=product_service,
        province_id=province_id,
        district_id=district_id,
        number_of_employees=number_of_employees,
        asset_value=asset_value,
        annual_revenue=annual_revenue
    )
    return sme


def determine_size_of_employees(number_of_employees):
    """Determine the size of employees based on the number of employees."""
    if number_of_employees < 5:
        return SizeValue.objects.get(size='MICRO')
    elif 5 <= number_of_employees <= 40:
        return SizeValue.objects.get(size='SMALL')
    elif 41 <= number_of_employees <= 75:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def determine_size_of_annual_revenue(annual_revenue):
    """Determine the size of annual revenue based on the annual revenue."""
    if annual_revenue <= 30000:
        return SizeValue.objects.get(size='MICRO')
    elif annual_revenue <= 500000:
        return SizeValue.objects.get(size='SMALL')
    elif annual_revenue <= 1000000:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def determine_size_of_asset_value(asset_value):
    """Determine the size of asset value based on the asset value."""
    if asset_value <= 10000:
        return SizeValue.objects.get(size='MICRO')
    elif asset_value <= 500000:
        return SizeValue.objects.get(size='SMALL')
    elif asset_value <= 1000000:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value):
    """Calculate the rating based on the size of employees, annual revenue, and asset value."""
    return size_of_employees.value + size_of_annual_revenue.value + size_of_asset_value.value


def determine_business_size(rating):
    """Determine the size of the business based on the rating."""
    if rating < 4:
        return SizeValue.objects.get(size='MICRO')
    elif rating < 8:
        return SizeValue.objects.get(size='SMALL')
    elif rating < 10:
        return SizeValue.objects.get(size='MEDIUM')
    else:
        return SizeValue.objects.get(size='LARGE')


def create_calculation_scale(sme, size_of_employees, size_of_annual_revenue, size_of_asset_value,
                             rating, size_of_business):
    """Create a CalculationScale record."""
    CalculationScale.objects.create(
        sme=sme,
        size_of_employees=size_of_employees,
        size_of_annual_revenue=size_of_annual_revenue,
        size_of_asset_value=size_of_asset_value,
        rating=rating,
        size_of_business=size_of_business
    )
