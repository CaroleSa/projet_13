#! /usr/bin/env python3
# coding: UTF-8

""" views to the account app """

# Imports
import re
import calendar
import locale
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, logout, \
    login as auth_login, update_session_auth_hash
from .forms import CreateAccountForm
from .models import HistoryUser, StatusUser
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
# pylint: disable=no-member


def create_account(request):
    """ create_account view """
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

        # checks the validity of the password,
        # email and pseudo format
        dict_regex_error = {password: [r"^[a-zA-Z0-9$@%*+\-_!\S]+$",
                                       "Mot de passe non valide : "
                                       "peut contenir lettres, "
                                       "chiffres ou symboles $@%*+\-_! "
                                       "sans espace. Doit être composé de 8 "
                                       "caractères minimum."],
                            email: [r"^[a-z0-9-_.]+@[a-z0-9-]+\.(com|fr)$",
                                    "Adresse e-mail non valide."],
                            pseudo: [r"^[a-zA-Z0-9\S]+$",
                                     "Pseudo non valide : peut contenir lettres "
                                     "ou chiffres, sans espace ni symbole."]}
        for data, regex_message in dict_regex_error.items():
            regex = regex_message[0]
            result = re.match(regex, data)
            if result is None:
                context["error_message"] = regex_message[1]
                return render(request, "dietetic/index.html", context)

        # create user's account
        # and login user
        if form.is_valid() is True:
            logout(request)
            user = user.objects.create_user(username=pseudo, email=email, password=password)
            HistoryUser.objects.create(user=user)
            StatusUser.objects.create(user=user)
            auth_login(request, user)
            context = {"create_account": "False",
                       "confirm_message": "Votre compte a bien été créé.",
                       "login_message": "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}

        # create an other
        # error message
        else:
            try:
                user = user.objects.get(email=email)
                context["error_message"] = "Ce compte existe déjà."
                is_active = StatusUser.objects.values_list("is_active").get(user=user.id)[0]
                if is_active is False:
                    context["error_message"] = "Ce compte a été supprimé et n'est pas réutilisable."
            except user.DoesNotExist:
                context["error_message"] = "Formulaire non valide."

    return render(request, "dietetic/index.html", context)


def login(request):
    """ login view """
    user = get_user_model()

    # create a context
    context = {}

    # get data
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_authenticate = authenticate(email=email, password=password)

        try:
            id_user = user.objects.values_list("id").get(email=email)
            is_active = StatusUser.objects.values_list("is_active").get(user=id_user)[0]

            # login user if the user exists
            # and if this account is activate
            if user_authenticate and is_active is True:
                auth_login(request, user_authenticate)
                pseudo = request.user.username
                context = {'login_message': "Bonjour {} ! Vous êtes bien connecté.".format(pseudo)}

            # create an error message
            # if the user don't exists
            # or if the password is false
            else:
                if is_active is False:
                    context["error_message"] = "Ce compte a été supprimé."
                else:
                    user.objects.get(email=email)
                    context["error_message"] = "Le mot de passe est incorrect."
        except user.DoesNotExist:
            context["error_message"] = "Ce compte n'existe pas."
        except StatusUser.DoesNotExist:
            context["error_message"] = "Ce compte n'y a pas accès."

    return render(request, "dietetic/index.html", context)


def my_account(request):
    """ my_account view """
    # get user's data
    email = request.user.email
    pseudo = request.user.username
    date_data = HistoryUser.objects.values_list("date_joined").get(user=request.user.id)
    date_create_account_list = re.findall(r"\d+", str(date_data))[0:3]
    date_create_account_str = ""+date_create_account_list[2]+" "\
                              +calendar.month_name[int(date_create_account_list[1])]\
                              +" "+date_create_account_list[0]+""
    context = {"date_create_account": date_create_account_str,
               "email": email, "pseudo": pseudo}

    if request.method == 'POST':

        # if the user clicks on the logo
        # "supprimer mon compte"
        # user's account is deactivate
        delete_account = request.POST.get('delete_account', 'False')
        if delete_account == 'True':
            user = StatusUser.objects.get(user=request.user.id)
            logout(request)
            user.is_active = False
            user.save()
            context = {'error_message': "Votre compte a bien été supprimé."}
            return render(request, "dietetic/index.html", context)

        # edit user's password
        user = get_user_model()
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        user_authenticate = authenticate(email=email, password=password)
        if user_authenticate:
            regex = r"^[a-zA-Z0-9$@%*+\-_!\S]+$"
            result = re.match(regex, new_password)
            if result is None:
                context["error_new_password"] = "invalide"
            else:
                user = user.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                context["confirm_message"] = "Votre mot de passe a bien été modifié."
        else:
            context["error_actual_password"] = "incorrect"

    return render(request, "account/my_account.html", context)
