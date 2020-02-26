#! /usr/bin/env python3
# coding: UTF-8

""" views of the account app """

# Imports
from django.shortcuts import render
from .forms import CreateAccountForm
import re
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login

def create_account(request):
    user = get_user_model()

    # create a context
    form = CreateAccountForm()
    context = {'form_create_account': form, "create_account": "True"}

    # get data
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        pseudo = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, pseudo, password, form.is_valid(), form.errors.as_data().items())

        # create an error message if the user's account exists
        if form.is_valid() is False:
            try:
                user.objects.get(email=email)
                context["error_message"] = "Ce compte existe déjà."
            except user.DoesNotExist:
                pass

        # create an error message if email isn't valid
        if form.is_valid() is True:
            regex = r"^[a-z0-9-_.]+@[a-z0-9-]+\.(com|fr)$"
            result = re.match(regex, email)
            if result is None:
                context["error_message"] = ["Adresse e-mail non valide."]

            # create user's account and login user
            else:
                user = user.objects.create_user(username=pseudo, email=email, password=password)
                auth_login(request, user)
                context = {"create_account": "False", "confirm_message": "Votre compte a bien été créé."}

    return render(request, "dietetic/index.html", context)


def login(request):
    context = {}
    return render(request, "dietetic/index.html", context)

def my_account(request):
    context = {}
    return render(request, "account/my_account.html", context)
