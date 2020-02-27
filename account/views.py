#! /usr/bin/env python3
# coding: UTF-8

""" views of the account app """

# Imports
from django.shortcuts import render
from .forms import CreateAccountForm, LoginForm
import re
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login
from .models import HistoryUser, IdentityUser, StatusUser
import calendar
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')
'fr_FR'


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

        # checks the validity of the password, email and pseudo format
        dict = {password: [r"^[a-zA-Z0-9$@%*+\-_!\S]+$", "Mot de passe non valide : peut contenir lettres, "
                                                         "chiffres ou symboles $@%*+\-_! sans espace. "
                                                         "Doit être composé de 8 caractères minimum."],
                email: [r"^[a-z0-9-_.]+@[a-z0-9-]+\.(com|fr)$", "Adresse e-mail non valide."],
                pseudo: [r"^[a-zA-Z0-9\S]+$", "Pseudo non valide : peut contenir lettres ou chiffres, "
                                              "sans espace ni symbole."]}
        for data, regex_message in dict.items():
            regex = regex_message[0]
            result = re.match(regex, data)
            if result is None:
                context["error_message"] = regex_message[1]
                return render(request, "dietetic/index.html", context)

        # create user's account and login user
        if form.is_valid() is True:
            user = user.objects.create_user(username=pseudo, email=email, password=password)
            HistoryUser.objects.create(user=user)
            StatusUser.objects.create(user=user)
            auth_login(request, user)
            context = {"create_account": "False",
                       "confirm_message": "Votre compte a bien été créé.",
                       "login_message": "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}
        # create an other error message
        else:
            try:
                user.objects.get(email=email)
                context["error_message"] = "Ce compte existe déjà."
            except user.DoesNotExist:
                context["error_message"] = "Formulaire non valide."

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
        user = user.objects.get(id=user_authenticate.id)

        # login user if the user exists
        if user_authenticate and user.is_active is True:
            auth_login(request, user_authenticate)
            pseudo = request.user.username
            context = {'login_message': "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}

        # create an error message if the user don't exists
        # or if the password is false
        else:
            if user.is_active is True:
                context["error_message"] = "Ce compte a été supprimé."
            try:
                user.objects.get(email=email)
                context["error_message"] = "Le mot de passe est incorrect."
            except user.DoesNotExist:
                context["error_message"] = "Ce compte n'existe pas."

    return render(request, "dietetic/index.html", context)


def my_account(request):
    user = get_user_model()

    # get user's data
    data = HistoryUser.objects.values_list("date_joined")
    date_data = data.get(user=request.user.id)
    date_create_account_list = re.findall('\d+', str(date_data))[0:3]
    date_create_account_str = ""+date_create_account_list[2]+" "+calendar.month_name[int(date_create_account_list[1])]+" "+date_create_account_list[0]+""

    email = request.user.email
    pseudo = request.user.username

    context = {"date_create_account": date_create_account_str, "email": email, "pseudo": pseudo}
    return render(request, "account/my_account.html", context)
