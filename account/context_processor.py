#! /usr/bin/env python3
# coding: UTF-8

""" Context processor """


# Imports
from django.conf import settings
from .forms import LoginForm


def login_form(request):
    form = LoginForm()
    return {'form_login': form}


def authentication_status(request):
    if request.user.is_authenticated:
        return {'authenticated': 'True'}

    return {'authenticated': 'False'}
