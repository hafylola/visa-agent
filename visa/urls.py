from django.urls import path
from api.views import visa_agent, health_check

urlpatterns = [
    path('a2a/agent/visa-agent', visa_agent, name='visa_agent'),
    path('', health_check, name='health_check'),
]