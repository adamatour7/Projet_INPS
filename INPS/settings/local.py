# settings/local.py

from .base import *
print("Local settings loaded.")

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
#ALLOWED_HOSTS = []

# Configuration de la base de données pour l'environnement de développement
DATABASES = {
    'default': {
        'NAME': 'INPS',
        'ENGINE': 'django.db.backends.mysql',  #  MySQLdb
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'At70812734',
        
    }
}
# Autres configurations spécifiques au développement
