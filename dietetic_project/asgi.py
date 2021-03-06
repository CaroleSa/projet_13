#! /usr/bin/env python3
# coding: UTF-8

"""
ASGI config for dietetic_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# imports
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dietetic_project.settings')

application = get_asgi_application()
