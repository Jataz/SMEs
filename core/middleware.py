from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return  # Skip if user is not logged in

        last_activity = request.session.get('last_activity')

        if last_activity:
            last_activity_time = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_activity_time > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                logout(request)
                request.session.flush()  # Clear session
                return  # Redirect to login will be handled by Django

        # Update session activity timestamp
        request.session['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
