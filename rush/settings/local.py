from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

FACEBOOK_APP_ID = '520402078044789'
FACEBOOK_APP_SECRET = '21636b80c9d8e6d1133f652d3a4c28a7'

INSTALLED_APPS += ('debug_toolbar',)

HOSTNAME = "http://0.0.0.0:8000"