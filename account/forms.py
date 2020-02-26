#! /usr/bin/env python3
# coding: UTF-8

""" ModelForm """


# Imports
from django.forms import ModelForm, TextInput, EmailInput, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class LoginForm(ModelForm):
    """ ModelForm LoginForm
    model : custom User
    fields : email and password """

    class Meta:
        """ Meta class """
        model = get_user_model()
        fields = ["email", "password"]
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password',
                                         'maxlength': '8', 'minlength': "8"})
        }


class CreateAccountForm(ModelForm):
    """ ModelForm CreateAccountForm
    model : custom User
    fields : username, email and password """

    class Meta:
        """ Meta class """
        model = get_user_model()
        fields = ["username", "email", "password"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password',
                                         'maxlength': '8', 'minlength': "8"})
        }


