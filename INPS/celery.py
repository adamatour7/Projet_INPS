from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir les paramètres de Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobile.settings')

app = Celery('mobile')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches automatiquement
app.autodiscover_tasks()

##

from celery.schedules import crontab

app.conf.beat_schedule = {
    'envoyer-les-rappels-cotisation-le-10': {
        'task': 'myapp.tasks.envoyer_rappels_cotisations',
        'schedule': crontab(day_of_month='10', hour=7, minute=30),  # Exécution le 10 à 7h30
    },
    'envoyer-les-rappels-cotisation-le-11': {
        'task': 'myapp.tasks.envoyer_rappels_cotisations',
        'schedule': crontab(day_of_month='11', hour=7, minute=30),  # Exécution le 11 à 7h30
    },
    'envoyer-les-rappels-cotisation-le-12': {
        'task': 'myapp.tasks.envoyer_rappels_cotisations',
        'schedule': crontab(day_of_month='12', hour=7, minute=30),  # Exécution le 12 à 7h30
    },
}
