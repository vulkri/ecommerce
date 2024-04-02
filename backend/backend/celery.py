from __future__ import absolute_import, unicode_literals
import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'remainder-email-cron-30s': {
        'task': 'orders.tasks.send_payment_remainder_mail',
        'schedule': 30.0,
        'args': ()
    },
}
