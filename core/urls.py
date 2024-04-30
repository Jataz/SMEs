from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('smeapp.urls')),
    path('',include('smeapp.urls')),
    path('', RedirectView.as_view(url='/login/')),
]
