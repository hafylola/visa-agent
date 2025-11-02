from django.urls import path
from api.views import visa_agent

urlpatterns = [
    path('a2a/agent/visa-agent', visa_agent, name='visa_agent'),
]
