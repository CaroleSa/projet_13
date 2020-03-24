#! /usr/bin/env python3
# coding: UTF-8

""" ModelForm """


# Imports
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from account.models import ProfileUser


class LoginForm(ModelForm):
    """ ModelForm LoginForm
    model : custom User
    fields : email and password """

    class Meta:
        """ Meta class """
        model = get_user_model()
        fields = ["email", "password"]
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control center'}),
            'password': TextInput(attrs={'class': 'form-control center', 'type': 'password',
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
            'username': TextInput(attrs={'class': 'form-control center', 'id': 'pseudo'}),
            'email': EmailInput(attrs={'class': 'form-control center', 'id': 'id_email'}),
            'password': TextInput(attrs={'class': 'form-control center', 'type': 'password',
                                         'maxlength': '8', 'minlength': "8",
                                         'id': 'password'})
        }
