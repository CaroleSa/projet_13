#! /usr/bin/env python3
# coding: UTF-8

""" ModelForm """


# Imports
from django.forms import ModelForm, TextInput, EmailInput
from django.conf import settings


class Account(ModelForm):
    """ ModelForm Account
    model : custom User
    fields : username, email and password """

    class Meta:
        """ Meta class """
        model = settings.AUTH_USER_MODEL
        fields = ["username", "email", "password"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password',
                                         'maxlength': '8', 'minlength':"8"})
        }
