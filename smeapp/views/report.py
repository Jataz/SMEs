from ..models import SME, CalculationScale,SizeValue,Sector
from django.http import JsonResponse
from django.db.models import Count, Avg, F

# API for each report
def demographic_report_api(request):
    data = SME.objects.values(province_name=F('province__province_name')).annotate(
        number_of_businesses=Count('id')
    ).order_by('-number_of_businesses')
    response_data = {
        'labels': [item['province_name'] for item in data],
        'values': [item['number_of_businesses'] for item in data],
    }
    return JsonResponse(response_data)

def business_size_report_api(request):
    data = CalculationScale.objects.values(size_name=F('size_of_business__size')).annotate(
        number_of_businesses=Count('id')
    ).order_by('-number_of_businesses')
    response_data = {
        'labels': [item['size_name'] for item in data],
        'values': [item['number_of_businesses'] for item in data],
    }
    return JsonResponse(response_data)

def compliance_report_api(request):
    data = SME.objects.values(compliance_status=F('tax')).annotate(
        count=Count('id')
    ).order_by('-count')
    response_data = {
        'labels': [item['compliance_status'] for item in data],
        'values': [item['count'] for item in data],
    }
    return JsonResponse(response_data)

def financial_performance_report_api(request):
    data = SME.objects.values(sector_name=F('sector__name')).annotate(
        avg_annual_turnover=Avg('annual_revenue')
    ).order_by('-avg_annual_turnover')
    response_data = {
        'labels': [item['sector_name'] for item in data],
        'values': [item['avg_annual_turnover'] for item in data],
    }
    return JsonResponse(response_data)

def export_report_api(request):
    data = SME.objects.values(export_status=F('export')).annotate(
        count=Count('id')
    ).order_by('-count')
    response_data = {
        'labels': [item['export_status'] for item in data],
        'values': [item['count'] for item in data],
    }
    return JsonResponse(response_data)

def training_education_report_api(request):
    data = SME.objects.values(education_level=F('education')).annotate(
        number_of_business_owners=Count('id')
    ).order_by('-number_of_business_owners')
    response_data = {
        'labels': [item['education_level'] for item in data],
        'values': [item['number_of_business_owners'] for item in data],
    }
    return JsonResponse(response_data)

# Age Range Distribution API
def age_range_report_api(request):
    age_ranges = {
        "18-25": [18, 25],
        "26-35": [26, 35],
        "36-45": [36, 45],
        "46-55": [46, 55],
        "56+": [56, 100],
    }

    data = [
        {
            "age_range": key,
            "count": SME.objects.filter(
                age__gte=value[0],
                age__lte=value[1]
            ).count(),
        }
        for key, value in age_ranges.items()
    ]

    response_data = {
        "labels": [item["age_range"] for item in data],
        "values": [item["count"] for item in data],
    }
    return JsonResponse(response_data)

from django.http import JsonResponse
from django.db.models import Count, Case, When, Value

def combined_report_api(request):
    # Demographic Report (Businesses by Province)
    demographic_data = SME.objects.values(province_name=F('province__province_name')).annotate(
        number_of_businesses=Count('id')
    ).order_by('-number_of_businesses')

    # Gender Report (Male, Female)
    gender_data = SME.objects.values(sex=F('sex')).annotate(
        count=Count('id')
    ).order_by('-count')

    # Age Range Report
    age_ranges = {
        "18-25": [18, 25],
        "26-35": [26, 35],
        "36-45": [36, 45],
        "46-55": [46, 55],
        "56+": [56, 100],
    }
    age_data = [
        {
            "age_range": key,
            "count": SME.objects.filter(
                age__gte=value[0],
                age__lte=value[1]
            ).count(),
        }
        for key, value in age_ranges.items()
    ]

    # Compliance Report
    compliance_data = SME.objects.values(compliance_status=F('tax')).annotate(
        count=Count('id')
    ).order_by('-count')

    # Financial Performance Report
    financial_performance_data = SME.objects.values(sector_name=F('sector__name')).annotate(
        avg_annual_turnover=Avg('annual_revenue')
    ).order_by('-avg_annual_turnover')

    # Export Status Report
    export_data = SME.objects.values(export_status=F('export')).annotate(
        count=Count('id')
    ).order_by('-count')

    # Combine all data into one response
    response_data = {
        "demographic": {
            "labels": [item['province_name'] for item in demographic_data],
            "values": [item['number_of_businesses'] for item in demographic_data],
        },
        "gender": {
            "labels": [item['sex'] for item in gender_data],
            "values": [item['count'] for item in gender_data],
        },
        "age_range": {
            "labels": [item['age_range'] for item in age_data],
            "values": [item['count'] for item in age_data],
        },
        "compliance": {
            "labels": [item['compliance_status'] for item in compliance_data],
            "values": [item['count'] for item in compliance_data],
        },
        "financial_performance": {
            "labels": [item['sector_name'] for item in financial_performance_data],
            "values": [item['avg_annual_turnover'] for item in financial_performance_data],
        },
        "export": {
            "labels": [item['export_status'] for item in export_data],
            "values": [item['count'] for item in export_data],
        },
    }

    return JsonResponse(response_data)

