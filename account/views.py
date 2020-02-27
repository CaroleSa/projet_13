#! /usr/bin/env python3
# coding: UTF-8

""" views of the account app """

# Imports
from django.shortcuts import render
from .forms import CreateAccountForm, LoginForm
import re
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login

def create_account(request):
    user = get_user_model()

    # create a context
    form = CreateAccountForm()
    context = {'form_create_account': form, "create_account": "True"}
    print("Carole", request.method)
    # get data
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        pseudo = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("erreurici", email, form.is_valid(), form.errors.as_data().items())
        # create an error message if the user's account exists
        if form.is_valid() is False:
            regex = r"^[a-z0-9-_.]+@[a-z0-9-]+\.(com|fr)$"
            result = re.match(regex, email)
            if result is None:
                context["error_message"] = "Adresse e-mail non valide."
            else:
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
                context["error_message"] = "Adresse e-mail non valide."

            # create user's account and login user
            else:
                user = user.objects.create_user(username=pseudo, email=email, password=password)
                auth_login(request, user)
                context = {"create_account": "False",
                           "confirm_message": "Votre compte a bien été créé.",
                           "login_message": "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}

    return render(request, "dietetic/index.html", context)


def login(request):
    user = get_user_model()

    # create a context
    context = {}

    # get data
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_authenticate = authenticate(email=email, password=password)

        # login user if the user exists
        if user_authenticate:
            auth_login(request, user_authenticate)
            pseudo = request.user.username
            context = {'login_message': "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}

        # create an error message if the user don't exists
        # or if the password is false
        else:
            try:
                user.objects.get(email=email)
                context["error_message"] = "Le mot de passe est incorrect."
            except user.DoesNotExist:
                context["error_message"] = "Ce compte n'existe pas."

    return render(request, "dietetic/index.html", context)


def my_account(request):
    context = {}
    return render(request, "account/my_account.html", context)
