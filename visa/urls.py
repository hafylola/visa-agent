from django.urls import path
from api.views import visa_agent
from api.views import health_check

urlpatterns = [
    path('', health_check),  # Add this line
    path('a2a/agent/visa-agent', visa_agent, name='visa_agent'),
]

