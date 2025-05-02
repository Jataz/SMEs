from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path,include

admin.site.site_header = "Adminstrator Dashboard"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to the Adminstrator Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('smeapp.urls')),
    path('',include('smeapp.urls')),
    path('', RedirectView.as_view(url='/login/')),
]
