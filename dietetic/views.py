#! /usr/bin/env python3
# coding: UTF-8

""" views of the dietetic app """

# Imports
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
import datetime
from .classes.controller import Controller
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser


def index(request):
    context = {}

    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')
    if logout_user == 'True':
        logout(request)

    return render(request, 'dietetic/index.html', context)


def dietetic_space(request):
    # get data
    id_user = request.user.id
    old_robot_question = request.POST.get('question', False)
    weekly_weight = request.POST.get('weekly_weight', False)
    height = request.POST.get('height', False)
    actual_weight = request.POST.get('actual_weight', False)
    cruising_weight = request.POST.get('cruising_weight', False)
    weight_goal = request.POST.get('weight_goal', False)
    data_weight_user = {"height": height, "actual_weight": actual_weight,
                        "cruising_weight": cruising_weight, "weight_goal": weight_goal}
    user_answer = request.POST.get('answer')

    # call controller_dietetic_space_view method and get context dict
    new_controller = Controller()
    context = new_controller.controller_dietetic_space_view(id_user, old_robot_question,
                                                            data_weight_user, user_answer,
                                                            weekly_weight)
    print(context)
    return render(request, 'dietetic/dietetic_space.html', context)


def my_results(request):
    # get data
    user = get_user_model()
    id = user.objects.get(id=request.user.id)

    starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=id).first()[0]
    starting_weight = ResultsUser.objects.values_list("weight").filter(user=id).first()[0]
    last_weight = ResultsUser.objects.values_list("weight").filter(user=id).last()[0]
    lost_weight = starting_weight - last_weight
    goal = ProfileUser.objects.values_list("actual_goal_weight").get(user=id)[0]
    percentage_goal = round((lost_weight * 100) / goal, 0)

    context = {"starting_date": starting_date, "starting_weight": starting_weight, "goal": goal,
               "percentage_goal": percentage_goal}




    """last_date = [2020, 7, 20]
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
            text = "Dernières pertes mauvaises !"""""



    return render(request, 'dietetic/my_results.html', context)


def program(request):
    context = {}

    return render(request, 'dietetic/program.html', context)
