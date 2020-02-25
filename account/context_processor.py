#! /usr/bin/env python3
# coding: UTF-8

""" Context processor """


# Imports
from django.conf import settings
from .forms import LoginForm


def login_form(request):
    form = LoginForm()
    return {'form': form}
