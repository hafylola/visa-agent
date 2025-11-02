import os
import sys

# Add your project to the path
sys.path.append('/app')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visa.settings')

# Import and create Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
