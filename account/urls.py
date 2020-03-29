#! /usr/bin/env python3
# coding: UTF-8

"""
URLS
Account app
"""


# imports
from django.conf.urls import url
from account import views


app_name = 'account'

urlpatterns = [
    url(r'^create_account/$', views.create_account, name="create_account"),
    url(r'^my_account/$', views.my_account, name="my_account"),
    url(r'^login/$', views.login, name="login")
]
