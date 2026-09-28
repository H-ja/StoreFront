import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
celery = Celery('storefront')
celery.config_from_object('django.conf:settings', namespace='CELERY')
# NOTE: using namespace all our settings configuration will start with 'CELERY'
celery.autodiscover_tasks()

# starting celery --> cmd: python -m celery -A storefront worker --loglevel=info
