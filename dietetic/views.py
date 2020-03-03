from django.shortcuts import render
from django.contrib.auth import get_user_model, logout


def index(request):
    context = {}
    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')

    if logout_user == 'True':
        logout(request)

    return render(request, 'dietetic/index.html', context)


def dietetic_space(request):
    context = {}

    if request.method == 'POST':
        list_robot_text = ["Nous allons tout d'abord définir ton objectif.", "Quelle taille fais-tu ?",
                           "Quel est ton poids actuel ?",
                           "Quel est ton poids de croisière (poids le plus longtemps maintenu sans effort) ?",
                           "Quel est ton poids d'objectif ?"]

        actual_weight = 60
        cruising_weight = 55
        goal_weight = 50
        height = 1.60

        actual_imc = actual_weight/(height*height)
        goal_imc = goal_weight/(height*height)
        cruising_imc = cruising_weight/(height*height)

        if actual_imc < 18.5:
            text = "Ton poids actuel est déjà bien bas... je te déconseille de perdre plus de poids."
        if goal_imc < 18.5:
            height_min = 18.5*(height * height)
            text = "Ton objectif semble trop bas, je te conseille de ne pas aller au dessous de"\
                   +str(height_min)+" kg."
        else:
            if cruising_imc < 24 and goal_weight < cruising_weight:
                text = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                       "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                       "aille en dessous de ce poids. Il est donc fortement" \
                       "possible que tu n'arrives pas à le maintenir sur la durée."

        total_goal = actual_weight - goal_weight
        if total_goal > 5:
            text = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                   "Je te propose donc de prévoir un premier objectif puis un second, ..."
            second_goal = total_goal-5
            text = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
                   "Passons maintenant à la suite du questionnaire."
            if second_goal <= 3:
                actual_goal = total_goal/2
                text = "Ton premier objectif serra donc de perdre "+str(actual_goal)+\
                       " kg. C'est parti ! Passons maintenant à la suite du questionnaire."
        else:
            text = "Alors c'est parti ! Partons sur un objectif de " + str(
                goal_weight) + " kg. Passons maintenant à la suite du questionnaire."

    return render(request, 'dietetic/dietetic_space.html', context)


def my_results(request):
    context = {}
    return render(request, 'dietetic/my_results.html', context)


def program(request):
    context = {}
    return render(request, 'dietetic/program.html', context)
