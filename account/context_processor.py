#! /usr/bin/env python3
# coding: UTF-8

""" Context processor """


# Imports
from django.conf import settings
from .forms import Account


def login_form(request):
    form = Account()
    return {'form': form}
