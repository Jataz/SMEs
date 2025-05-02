from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from rest_framework import status,generics,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from .Calculations import calculate_rating, create_calculation_scale, determine_business_size, determine_size_of_annual_revenue, determine_size_of_asset_value,\
    determine_size_of_employees,update_calculation_scale,update_sme_record_in_database

from ..models import SME,Province,District, Sector,SizeValue,CalculationScale, UserProfile, Ward

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
            matched_smes = SME.objects.all().order_by('-created_at')
        else:
            # Get the logged-in user's profile
            user_profile = get_object_or_404(UserProfile, user=user)

            # Initialize matched_smes queryset
            matched_smes = SME.objects.none()

            # Filter SMEs based on the user's access level
            if user_profile.is_national_level:
                matched_smes = SME.objects.all().order_by('-created_at')
            elif user_profile.is_province_level:
                matched_smes = SME.objects.filter(province=user_profile.province).order_by('-created_at')
            elif user_profile.is_district_level:
                matched_smes = SME.objects.filter(district=user_profile.district).order_by('-created_at')
            elif user_profile.is_ward_level:
                matched_smes = SME.objects.filter(ward=user_profile.ward).order_by('-created_at')

        # Serialize SMEs along with related calculation scales and size values
        serializer = SMESerializer(matched_smes, many=True, context={'request': request})

        # Return serialized data
        return Response(serializer.data)

class SMEUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SME.objects.all()
    serializer_class = SMESerializer
  
@csrf_exempt
def sme_create_record(request):
    if request.method != 'POST':
        return JsonResponse({'Error': 'Method not allowed'}, status=405)

    try:
        # Parse the JSON payload
        form_data = json.loads(request.body)

        # Retrieve the logged-in user profile
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        # Fetch user location details from profile
        province_id = user_profile.province_id
        district_id = user_profile.district_id
        ward_id = user_profile.ward_id

        # Retrieve sector object
        sector_id = int(form_data.get('sector'))
        sector = Sector.objects.get(id=sector_id)

        # Extract other form data
        company = form_data.get('company')
        contact_person = form_data.get('contact_person')
        phone_number = form_data.get('phone_number')
        email = form_data.get('email')
        address = form_data.get('address') 
        type_of_business = form_data.get('type_of_business')
        product_service = form_data.get('product_service')
        number_of_employees = int(form_data.get('number_of_employees'))
        asset_value = float(form_data.get('asset_value'))
        annual_revenue = float(form_data.get('annual_revenue'))
        export = form_data.get('export')
        comments = form_data.get('comments')
        compliance = form_data.get('compliance')
        registration = form_data.get('registration')
        tax = form_data.get('tax')
        education = form_data.get('education')
        training_received = form_data.get('training_received')
        source_of_funds = form_data.get('source_of_funds')
        ownership = form_data.get('ownership')
        support_service = form_data.get('support_service')
        funding_received = form_data.get('funding_received')

        # Generate SME reference number
        sme_ref_number = f"SME{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Create the SME record
            sme = SME.objects.create(
                company=company,
                type_of_business=type_of_business,
                registration=registration,
                sector=sector,
                product_service=product_service,
                number_of_employees=number_of_employees, 
                export=export,
                ownership=ownership,  # New field, setting default None
                contact_person=contact_person,
                address=address,
                phone_number=phone_number,
                email=email,
                education=education,
                support_service=support_service,  # New field, setting default None
                training_received=training_received,  # Note spelling fixed from received
                funding_received=funding_received,  # New field, setting default None
                compliance=compliance,
                tax=tax,
                source_of_funds=source_of_funds,
                annual_revenue=annual_revenue,
                asset_value=asset_value,
                comments=comments,
                province_id=province_id,
                district_id=district_id,
                ward_id=ward_id,
                sme_ref_number=sme_ref_number
            )

            # Calculate sizes based on sector thresholds
            size_of_employees = determine_size_of_employees(number_of_employees, sector)
            size_of_annual_revenue = determine_size_of_annual_revenue(annual_revenue, sector)
            size_of_asset_value = determine_size_of_asset_value(asset_value, sector)

            # Calculate the rating and determine business size
            rating = calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value)
            size_of_business = determine_business_size(rating)

            # Create the CalculationScale record
            create_calculation_scale(
                sme=sme,
                size_of_employees=size_of_employees,
                size_of_annual_revenue=size_of_annual_revenue,
                size_of_asset_value=size_of_asset_value,
                rating=rating,
                size_of_business=size_of_business
            )

        return JsonResponse({'success': 'SME added successfully'}, status=201)

    except UserProfile.DoesNotExist:
        return JsonResponse({'Error': 'User profile not found. Please contact the Administrator to set up your account.'}, status=400)

    except Sector.DoesNotExist:
        return JsonResponse({'Error': 'Invalid sector provided.'}, status=400)

    except ValueError as ve:
        return JsonResponse({'Error': f'Invalid input data: {ve}'}, status=400)

    except Exception as e:
        return JsonResponse({'Error': f'An unexpected error occurred: {e}'}, status=400)




def update_sme_record(request):
    if request.method != 'PUT':
        return JsonResponse({'Error': 'Method not allowed'}, status=405)

    try:
        form_data = json.loads(request.body)

        # Retrieve form data
        sme_id = form_data.get('smeId')
        company = form_data.get('company')
        contact_person = form_data.get('contact_person')
        phone_number = form_data.get('phone_number')
        email = form_data.get('email')
        address = form_data.get('address')
        sector = form_data.get('sector')  # Retrieve sector ID
        type_of_business = form_data.get('type_of_business')
        product_service = form_data.get('product_service')
        number_of_employees = int(form_data.get('number_of_employees'))
        asset_value = float(form_data.get('asset_value'))
        annual_revenue = float(form_data.get('annual_revenue'))
        export = form_data.get('export')
        comments = form_data.get('comments')
        compliance = form_data.get('compliance')
        registration = form_data.get('registration')
        tax = form_data.get('tax')
        education = form_data.get('education')
        training_received = form_data.get('training_received')
        source_of_funds = form_data.get('source_of_funds')
        ownership = form_data.get('ownership')
        support_service = form_data.get('support_service')
        funding_received = form_data.get('funding_received')

        # Validate required fields
        missing_fields = []
        required_fields = {
            'sme_id': sme_id,
            'company': company,
            'contact_person': contact_person,
            'phone_number': phone_number,
            'email': email,
            'address': address,
            'sector': sector,
            'type_of_business': type_of_business,
            'product_service': product_service,
            'number_of_employees': number_of_employees,
            'asset_value': asset_value,
            'annual_revenue': annual_revenue,
            'export': export,
            'comments': comments,
            'compliance': compliance,
            'registration': registration,
            'tax': tax,
            'education': education,
            'source_of_funds': source_of_funds,
            'ownership': ownership,
            'support_service': support_service,
        }

        # Check each field explicitly
        for field, value in required_fields.items():
            if value is None or value == '':
                missing_fields.append(field)

        if missing_fields:
            return JsonResponse({'Error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)

        try:
            # Retrieve the sector object
            sector = Sector.objects.get(id=sector)
        except Sector.DoesNotExist:
            return JsonResponse({'Error': 'Invalid sector provided.'}, status=400)

        # Start a database transaction
        with transaction.atomic():
            # Update SME record
            SME.objects.filter(id=sme_id).update(
                company=company,
                type_of_business=type_of_business,
                registration=registration,
                sector=sector,
                product_service=product_service,
                number_of_employees=number_of_employees,
                export=export,
                ownership=ownership,
                contact_person=contact_person,
                address=address,
                phone_number=phone_number,
                email=email,
                education=education,
                support_service=support_service,
                training_received=training_received,
                funding_received=funding_received,
                compliance=compliance,
                tax=tax,
                source_of_funds=source_of_funds,
                annual_revenue=annual_revenue,
                asset_value=asset_value,
                comments=comments
            )

            # Calculate sizes based on sector-specific thresholds
            size_of_employees = determine_size_of_employees(number_of_employees, sector)
            size_of_annual_revenue = determine_size_of_annual_revenue(annual_revenue, sector)
            size_of_asset_value = determine_size_of_asset_value(asset_value, sector)

            # Calculate rating and determine business size
            rating = calculate_rating(size_of_employees, size_of_annual_revenue, size_of_asset_value)
            size_of_business = determine_business_size(rating)

            # Update or create CalculationScale record
            CalculationScale.objects.update_or_create(
                sme_id=sme_id,
                defaults={
                    'size_of_employees': size_of_employees,
                    'size_of_annual_revenue': size_of_annual_revenue,
                    'size_of_asset_value': size_of_asset_value,
                    'rating': rating,
                    'size_of_business': size_of_business
                }
            )

            return JsonResponse({'success': 'SME updated successfully.'}, status=200)

    except ValueError as ve:
        return JsonResponse({'Error': f'Invalid input data: {ve}'}, status=400)

    except Exception as e:
        return JsonResponse({'Error': f'An unexpected error occurred: {str(e)}'}, status=400)

    

def update_sme_record_in_database(sme_id, company, contact_person, phone_number, email, address, sector,
                                  type_of_business, product_service,number_of_employees, asset_value, annual_revenue,
                                  export,comments,ownership, support_service, training_received, funding_received,
                                  source_of_funds,compliance, registration, tax, education):
    # Assuming you have a model for SME records and CalculationScale records
    sme = SME.objects.get(id=sme_id)
    sme.company = company
    sme.type_of_business = type_of_business
    sme.registration = registration
    sme.sector = sector
    sme.product_service = product_service
    sme.number_of_employees = number_of_employees
    sme.export = export
    sme.ownership = ownership
    sme.contact_person = contact_person
    sme.address = address
    sme.phone_number = phone_number
    sme.email = email
    sme.education = education
    sme.support_service = support_service
    sme.training_received = training_received
    sme.funding_received = funding_received
    sme.compliance = compliance
    sme.tax = tax
    sme.source_of_funds = source_of_funds
    sme.annual_revenue = annual_revenue
    sme.asset_value = asset_value
    sme.comments = comments
    sme.save()
    
    return sme