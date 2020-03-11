#! /usr/bin/env python3
# coding: UTF-8

""" views of the dietetic app """

# Imports
from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model, logout
from django.http import JsonResponse
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
    final_weight = ProfileUser.objects.values_list("final_weight").get(user=id)[0]
    starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=id).first()[0]
    last_date = ResultsUser.objects.values_list("weighing_date").filter(user=id).last()[0]
    starting_weight = ResultsUser.objects.values_list("weight").filter(user=id).first()[0]
    last_weight = ResultsUser.objects.values_list("weight").filter(user=id).last()[0]

    # test
    results_weight_data = ResultsUser.objects.values_list("weight").filter(user=id)
    results_date_data = ResultsUser.objects.values_list("weighing_date").filter(user=id)
    list_data = [['Date', 'Poids']]
    for date, weight in zip(results_date_data, results_weight_data):
        list_date_weight = [date[0], weight[0]]
        list_data.append(list_date_weight)

    # test
    get_data = request.GET.get("get_data", "False")
    if get_data == "True":
        data = list_data
        return JsonResponse(data, safe=False)

    # calculates the percentage of lost weight
    total_lost_weight = float(starting_weight - last_weight)
    total_goal = float(starting_weight - final_weight)
    lost_percentage = int((total_lost_weight * 100) / total_goal)

    # calculates the average weight loss
    delta = last_date - starting_date
    number_of_weeks = delta.days/7
    try:
        average_lost_weight = total_lost_weight/number_of_weeks
    except ZeroDivisionError:
        average_lost_weight = 0

    display_info = False
    if starting_date != last_date:
        display_info = True

    context = {"starting_date": starting_date, "starting_weight": starting_weight, "total_goal": total_goal,
               "lost_percentage": lost_percentage, "average_lost_weight": average_lost_weight,
               "display_info": display_info, "list_data": list_data}

    return render(request, 'dietetic/my_results.html', context)


def program(request):
    context = {}

    return render(request, 'dietetic/program.html', context)
