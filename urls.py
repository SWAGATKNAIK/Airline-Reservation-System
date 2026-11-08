from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Keep the default admin available at /django-admin/ if you ever need it for debugging
    path('django-admin/', admin.site.urls),
    
    # Send everything else to the 'core' app
    path('', include('core.urls')),
]