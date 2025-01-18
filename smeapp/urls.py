
from django.urls import path

from .views import SMEListView,ProvinceAPIView,DistrictAPIView,WardAPIView,sme_create_record,size_of_business_data,\
            get_districts,get_wards,SmeDetail,SMEUpdateView,update_sme_record,sex_data,get_sectors
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sme-create/',sme_create_record,name="sme-create"),
    path('sme-detail/<int:pk>/', SmeDetail.as_view(), name='sme-detail'),
    path('sme-update/<int:pk>/', SMEUpdateView.as_view(), name='sme-update'),
    path('sme/update/', update_sme_record, name='update_sme_records'),
    path('sectors/', get_sectors, name='get_sectors'),
    
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
    
    #Testing    

]
