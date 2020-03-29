#! /usr/bin/env python3
# coding: UTF-8

"""
Context processor
account app
"""


# Imports
from django.conf import settings
from .forms import LoginForm


def login_form(request):
    """
    add login form
    in all contexts
    """
    form = LoginForm()
    return {'form_login': form}


def authentication_status(request):
    """
    login status
    in all contexts
    """
    if request.user.is_authenticated:
        return {'authenticated': 'True'}
    return {'authenticated': 'False'}
