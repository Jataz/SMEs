
from django.urls import path

from .views import SMEListView,SMECreate,ProvinceAPIView,DistrictAPIView,sme_record,size_of_business_data
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sme-create/',sme_record,name="sme-create"),
    path('size-of-business-data/', size_of_business_data, name='size_of_business_data'),

    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('districts/', DistrictAPIView.as_view(), name='districts'),

    #Frontend URLS
    path('dashboard/', views.index ,name='index'),
    path('sme-list/', views.sme_list, name='sme-list'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
    
    #Testing
    path('sme-record/', sme_record, name='sme-record'),
]