from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
import datetime
from .models import RobotAdvices, DiscussionSpace, RobotQuestion
from django.db.models import Avg, Count


def index(request):
    context = {}
    # PREVOIR CHARGEMENT DES DONNEES DE LINSTANTANE AUTOMATIQUE ICI

    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')
    if logout_user == 'True':
        logout(request)

    return render(request, 'dietetic/index.html', context)


def dietetic_space(request):
    context = {}

    # PROBLEME ERREUR QUERY
    user = get_user_model()
    user = user.objects.get(id=request.user.id)
    advices = RobotAdvices.objects.get(id=1)
    #user.advices_to_user.add(advices)
    #print("advices", user.advices_to_user.all())

    # PREVOIR METTRE ID AUTOINCREMENT POUR ORDRE DES QUESTIONS
    data = DiscussionSpace.objects.values_list("robot_question").order_by('id').annotate(count=Count('robot_question'))
    list_data = data
    id_list = []
    for elt in list_data:
        id_list.append(elt[0])
        robot_question = RobotQuestion.objects.values_list("text").get(id=elt)
        list(set(id_list))
        # liste des id des questions à poser
        print(robot_question)

    #id_last_discussion = DiscussionSpace.objects.values_list("id").last()[0]
    #id_list = list(range(1, id_last_discussion + 1))


    if request.method == 'POST':
        # si c'est sa première inscription sinon texte différent pour nouvel objectif
        list_robot_text = ["Nous allons tout d'abord définir ton objectif.", "Quelle taille fais-tu ?",
                           "Quel est ton poids actuel ?",
                           "Quel est ton poids de croisière (poids le plus longtemps maintenu sans effort) ?",
                           "Quel est ton poids d'objectif ?"]

        actual_weight = 60
        cruising_weight = 55
        goal_weight = 50
        height = 1.60

        actual_imc = round(actual_weight/(height*height), 1)
        goal_imc = round(goal_weight/(height*height), 1)
        cruising_imc = round(cruising_weight/(height*height), 1)

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

    starting_date = [2020, 5, 20]
    starting_weight = 60
    last_date = [2020, 7, 20]
    last_weight = 55
    starting_week = datetime.datetime(starting_date[0], starting_date[1], starting_date[2]).isocalendar()[1]
    last_week = datetime.datetime(last_date[0], last_date[1], last_date[2]).isocalendar()[1]
    number_week = last_week - starting_week
    lost_weight = starting_weight - last_weight
    average_weight_loss = round(lost_weight/number_week, 1)
    last_2_weighings = "ok"
    last_weighings = "ok"
    if average_weight_loss <= 0.3:
        text = "Petite moyenne de perte de poids"
    if average_weight_loss >= 0.4 <= 0.5:
        text = "Moyenne de perte de poids moyenne"
    if average_weight_loss >= 0.6 <= 0.8:
        text = "Bonne moyenne de perte de poids"
    if average_weight_loss >= 0.9:
        text = "Très bonne moyenne de perte de poids"

    if last_2_weighings == "ok":
        text = "Dernières pertes parfaites !"
    else:
        if last_weighings == "ok":
            text = "Dernières pertes moyennes !"
        else:
            text = "Dernières pertes mauvaises !"



    return render(request, 'dietetic/my_results.html', context)


def program(request):
    context = {}
    return render(request, 'dietetic/program.html', context)
