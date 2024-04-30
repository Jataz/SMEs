from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings

# Create your views here.

@login_required(login_url="/login")
def index(request):
 
  return render(request, 'pages/dashboard/index.html')

@login_required(login_url="/login")
def sme_list(request):
    # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/smes/',       
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        smes = response.json() # Extract JSON data from the response
        return render(request, 'pages/smes/index.html',{'smes':smes})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch SMEs data'})