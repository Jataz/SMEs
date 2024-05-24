from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from rest_framework import status,generics,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json

from .Calculations import calculate_rating, create_calculation_scale, determine_business_size, determine_size_of_annual_revenue, determine_size_of_asset_value,\
    determine_size_of_employees,update_calculation_scale,update_sme_record_in_database

from ..models import SME,Province,District,SizeValue,CalculationScale, UserProfile, Ward

from ..serializers import SMESerializer,ProvinceSerializer,DistrictSerializer,WardSerializer


class ProvinceAPIView(APIView):
    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response({'provinces': serializer.data})

class DistrictAPIView(APIView):
    def get(self, request):
        province_id = request.GET.get('province_id')
        districts = District.objects.filter(province_id=province_id).order_by('district_name')
        serializer = DistrictSerializer(districts, many=True)
        return Response({'districts': serializer.data})

class WardAPIView(APIView):
    def get(self, request):
        district_id = request.GET.get('district_id')
        wards = Ward.objects.filter(district_id=district_id).order_by('ward_name')
        serializer = WardSerializer(wards, many=True)
        return Response({'wards': serializer.data})
#For Admin Panel#
def get_districts(request, province_id):
    districts = list(District.objects.filter(province_id=province_id).values('id', 'district_name'))
    return JsonResponse({'districts': districts})

def get_wards(request, district_id):
    wards = list(Ward.objects.filter(district_id=district_id).values('id', 'ward_name'))
    return JsonResponse({'wards': wards})

class SmeDetail(APIView):
    def get(self, request, pk):
        try:
            sme = SME.objects.get(id=pk)
            serializer = SMESerializer(sme)
            return Response(serializer.data)
        except SME.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
class SMEListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # If the user is a superuser, return all SMEs
        if user.is_superuser:
            matched_smes = SME.objects.all()
        else:
            # Get the logged-in user's profile
            user_profile = get_object_or_404(UserProfile, user=user)

            # Initialize matched_smes queryset
            matched_smes = SME.objects.none()

            # Filter SMEs based on the user's access level
            if user_profile.is_national_level:
                matched_smes = SME.objects.all()
            elif user_profile.is_province_level:
                matched_smes = SME.objects.filter(province=user_profile.province)
            elif user_profile.is_district_level:
                matched_smes = SME.objects.filter(district=user_profile.district)
            elif user_profile.is_ward_level:
                matched_smes = SME.objects.filter(ward=user_profile.ward)

        # Serialize SMEs along with related calculation scales and size values
        serializer = SMESerializer(matched_smes, many=True, context={'request': request})

        # Return serialized data
        return Response(serializer.data)

class SMEUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SME.objects.all()
    serializer_class = SMESerializer
  
@csrf_exempt
def sme_create_record(request):
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
        ward_id =form_data.get('ward_id')
        number_of_employees = int(form_data.get('number_of_employees'))  # Convert to integer
        asset_value = form_data.get('asset_value')
        annual_revenue = form_data.get('annual_revenue')
        age = form_data.get('age')
        sex = form_data.get('sex')
        
        try:
            annual_revenue = int(form_data.get('annual_revenue'))
            asset_value = int(form_data.get('asset_value'))
        except ValueError:
            return JsonResponse({'error': 'Invalid value for annual revenue or asset value'}, status=400)

        
        # Validate form data
        if not all([company, contact_person, phone_number, email, address, sector, type_of_business, product_service,
                    province_id, district_id,ward_id, number_of_employees, asset_value, annual_revenue,age,sex]):
            return JsonResponse({'error': 'Please fill in all fields'}, status=400)
        
        # Start a database transaction
        with transaction.atomic():
            try:
                # Create SME record
                sme = create_sme_record(company, contact_person, phone_number, email, address, sector,
                                         type_of_business, product_service, province_id, district_id,ward_id,
                                         number_of_employees, asset_value, annual_revenue,age,sex)
                
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
                      type_of_business, product_service, province_id, district_id,ward_id,
                      number_of_employees, asset_value, annual_revenue,age,sex):
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
        ward_id=ward_id,
        number_of_employees=number_of_employees,
        asset_value=asset_value,
        annual_revenue=annual_revenue,
        age=age,
        sex=sex
    )
    return sme

def update_sme_record(request):
    if request.method == 'PUT':
        form_data = json.loads(request.body)
        
        # Retrieve form data
        sme_id = form_data.get('id')
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
        ward_id = form_data.get('ward_id')
        number_of_employees = form_data.get('number_of_employees')  # Convert to integer
        asset_value = form_data.get('asset_value')
        annual_revenue = form_data.get('annual_revenue')
        age = form_data.get('age')
        sex = form_data.get('sex')
        
        try:
            number_of_employees = int(form_data.get('number_of_employees'))
            annual_revenue = float(form_data.get('annual_revenue'))
            asset_value = float(form_data.get('asset_value'))
        except ValueError:
            return JsonResponse({'error': 'Invalid value for annual revenue or asset value'}, status=400)

        # Validate form data
        if not all([sme_id, company, contact_person, phone_number, email, address, sector, type_of_business,
                    product_service, province_id, district_id, ward_id, number_of_employees, asset_value,
                    annual_revenue, age, sex]):
            return JsonResponse({'error': 'Please fill in all fields'}, status=400)
        
        # Start a database transaction
        with transaction.atomic():
            try:
                # Update SME record
                update_sme_record_in_database(sme_id, company, contact_person, phone_number, email, address, sector,
                                              type_of_business, product_service, province_id, district_id, ward_id,
                                              number_of_employees, asset_value, annual_revenue, age, sex)
                
                # Determine rating based on number_of_employees, annual_revenue, and asset_value
                size_of_employees = determine_size_of_employees(number_of_employees)
                size_of_annual_revenue = determine_size_of_annual_revenue(annual_revenue)
                size_of_asset_value = determine_size_of_asset_value(asset_value)
                rating = calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value)
                
                # Determine the size of the business based on rating
                size_of_business = determine_business_size(rating)
                
                # Update CalculationScale record
                update_calculation_scale(sme_id, size_of_employees, size_of_annual_revenue, size_of_asset_value,
                                         rating, size_of_business)
                
                return JsonResponse({'success': 'SME updated successfully'}, status=200)
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)