#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic URLS """


# imports
from django.conf.urls import url
from dietetic import views


app_name = 'dietetic'

urlpatterns = [
    url(r'^my_results/$', views.my_results, name="my_results"),
    url(r'^dietetic_space/$', views.dietetic_space, name="dietetic_space"),
    url(r'^program/$', views.program, name="program")
]