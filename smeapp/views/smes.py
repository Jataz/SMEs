from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import SME,Province,District,SizeValue

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


class SMEListView(APIView):
    def get(self, request):
        smes = SME.objects.all()
        serializer = SMESerializer(smes, many=True)
        return Response(serializer.data)

class SMECreate(generics.CreateAPIView):
    queryset = SME.objects.all()
    serializer_class = SMESerializer
    
@csrf_exempt
def create_sme_record(request):
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
        
        # Validate form data
        if not all([company, contact_person, phone_number, email, address, sector, type_of_business, product_service,
                    province_id, district_id, number_of_employees, asset_value, annual_revenue]):
            return JsonResponse({'error': 'Please fill in all fields'}, status=400)
        
        # Determine size_of_business based on number_of_employees
        if number_of_employees < 5:
            size_category = 'MICRO'
        elif 5 <= number_of_employees <= 40:
            size_category = 'SMALL'
        elif 41 <= number_of_employees <= 75:
            size_category = 'MEDIUM'
        else:
            size_category = 'LARGE'
        
        # Fetch SizeValue object corresponding to the size_category
        try:
            size_value_obj = SizeValue.objects.get(size=size_category)
        except SizeValue.DoesNotExist:
            return JsonResponse({'error': 'SizeValue object not found for the specified category'}, status=400)

        # Create SME record
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
            size_of_business_id=size_value_obj.pk,
            asset_value=asset_value,
            annual_revenue=annual_revenue
        )
        
        return JsonResponse({'success': 'SME added successfully'}, status=201)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)