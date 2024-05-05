
from django.urls import path

from .views import SMEListView,SMECreate,ProvinceAPIView,DistrictAPIView,create_sme_record
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sm-create/', SMECreate.as_view(), name='sm-create'),
    path('sme-create/',create_sme_record,name="sme-create"),

    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('districts/', DistrictAPIView.as_view(), name='districts'),

    #Frontend URLS
    path('dashboard/', views.index ,name='index'),
    path('sme-list/', views.sme_list, name='sme-list'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
]