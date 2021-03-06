#! /usr/bin/env python3
# coding: UTF-8

"""
WSGI config for dietetic_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

# imports
import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dietetic_project.settings')
application = get_wsgi_application()
