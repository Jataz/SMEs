
from django.urls import path

from .views import SMEListView,SMECreate,ProvinceAPIView,DistrictAPIView,WardAPIView,sme_record,size_of_business_data
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sme-create/',sme_record,name="sme-create"),
    path('size-of-business-data/', size_of_business_data, name='size_of_business_data'),
    #path('sme/',sme_in_user_province, name='sme'),

    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('districts/', DistrictAPIView.as_view(), name='districts'),
    path('wards/', WardAPIView.as_view(), name='ward_data'),

    #Frontend URLS
    path('dashboard/', views.index ,name='index'),
    path('sme-list/', views.sme_list, name='sme-list'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
    
    #Testing
    path('sme-record/', sme_record, name='sme-record'),
]