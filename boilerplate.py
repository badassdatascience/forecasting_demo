#
# load system libraries
#
import sys
import os

#
# user settings
#
application_root_directory = os.environ['APP_HOME']

#
# set the path and environment
#
sys.path.append(application_root_directory + '/django_apps/infrastructure')
os.environ['DJANGO_SETTINGS_MODULE'] = 'infrastructure.settings'

#
# load Django 
#
import django
django.setup()
