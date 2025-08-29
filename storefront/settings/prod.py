import os
import dj_database_url 
from .common import *


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['storefront-prod.herokuapp.com']

# read the database from url in environment variables
DATABASES = {
    'default': dj_database_url.config()
    }