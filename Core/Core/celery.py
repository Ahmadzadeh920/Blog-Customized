import os

from celery import Celery

from celery.schedules import crontab
from accounts.tasks import sendEmail

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')

app = Celery("Core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

'''@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls send Email tasks ('hello') every 10 seconds.
    sender.add_periodic_task(10.0, sendEmail.s(), name='SendEmail every 10 seconds')'''

    




