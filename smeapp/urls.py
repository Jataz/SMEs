
from django.urls import path

from .views import ( SMEListView,ProvinceAPIView,DistrictAPIView,WardAPIView,sme_create_record,size_of_business_data,
            get_districts,get_wards,SmeDetail,SMEUpdateView,update_sme_record,sex_data,get_sectors,SMEReportsView, update_session,
            demographic_report_api,
            business_size_report_api,
            financial_performance_report_api,
            export_report_api,
            training_education_report_api,
            gender_api,
            age_api,
            )
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sme-create/',sme_create_record,name="sme-create"),
    path('sme-detail/<int:pk>/', SmeDetail.as_view(), name='sme-detail'),
    path('sme-update/<int:pk>/', SMEUpdateView.as_view(), name='sme-update'),
    path('sme/update/', update_sme_record, name='update_sme_records'),
    path('sectors/', get_sectors, name='get_sectors'),
    path('age-range-report/', views.age_range_report_filtered_view, name='age_range_report_filtered'),
    
    #Graphs
    path('size-of-business-data/', size_of_business_data, name='size_of_business_data'),
    path('sex-data/', sex_data, name='sex_data'),

    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('districts/', DistrictAPIView.as_view(), name='districts'),
    path('wards/', WardAPIView.as_view(), name='ward_data'),
    
    #Admin Panel
    path('admin/get_districts/<int:province_id>/', views.get_districts, name='get_districts'),
    path('admin/get_wards/<int:district_id>/', views.get_wards, name='get_wards'),

    #Frontend URLS
    path('dashboard/', views.index ,name='index'),
    path('sme-list/', views.sme_list, name='sme-list'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
    path('update-session/', update_session, name='update_session'),
    
    #Reports   
    path('reports/', SMEReportsView.as_view(), name='sme_reports'),
    path('api/demographic/', demographic_report_api, name='demographic_api'),
    path('api/business-size/', business_size_report_api, name='business_size_api'),
    path('api/financial-performance/', financial_performance_report_api, name='financial_performance_api'),
    path('api/export/', export_report_api, name='export_api'),
    path('api/training-education/', training_education_report_api, name='training_education_api'),
    path('api/gender/', gender_api, name='gender_api'),
    path('api/age/', age_api, name='age_api'),

]
