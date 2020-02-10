#! /usr/bin/env python3
# coding: UTF-8

""" Account URLS """


# imports
from django.conf.urls import url
from . import views


app_name = 'account'

urlpatterns = [
    url(r'^create_account/$', views.create_account, name="create_account")
]