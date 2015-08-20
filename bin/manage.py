#!/usr/bin/env python
import os
import sys

# Add the project to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

PROJECT_MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PROJECT_APPS_PATH = os.path.join(PROJECT_MODULE_PATH, 'ehb_service/apps')
PROJECT_ROOT, PROJECT_MODULE_NAME = os.path.split(PROJECT_MODULE_PATH)

# setup the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehb_service.conf.settings')
os.environ.setdefault('PYTHON_EGG_CACHE', '/tmp')

sys.path.insert(0, PROJECT_MODULE_PATH)
sys.path.insert(0, PROJECT_APPS_PATH)

from django.core.management import execute_from_command_line
execute_from_command_line()
