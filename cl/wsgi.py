import os
import sys

path = '/home/dhxvm/www'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'cl.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


