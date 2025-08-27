import os
from celery import Celery

# set default environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

# create a celery object and give it a name
celery = Celery('storefront')

# specify where celery can find configuration variable
celery.config_from_object('django.conf:settings', namespace='CELERY')

# run auto_discover_tasks
celery.autodiscover_tasks()