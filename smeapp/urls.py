
from django.urls import path

from .views import SMEListView,SMECreate
from . import views

urlpatterns =[
    #API
    path('smes/', SMEListView.as_view(), name='smes'),
    path('sme-create/', SMECreate.as_view(), name='sme-create'),
    #Frontend URLS
    path('dashboard/', views.index ,name='index'),
    path('sme-list/', views.sme_list, name='sme-list'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
]