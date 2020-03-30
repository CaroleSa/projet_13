#! /usr/bin/env python3
# coding: UTF-8

""" views of the dietetic app """

# Imports
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.http import JsonResponse
from account.models import ProfileUser, ResultsUser
from .classes.controller import Controller
from .classes.calculation import Calculation
# pylint: disable=no-member


def index(request):
    """ index view """
    context = {}

    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')
    if logout_user == 'True':
        logout(request)

    return render(request, 'dietetic/index.html', context)


def legal_notices(request):
    """ legal_notices view """
    context = {}

    return render(request, 'dietetic/legal_notices.html', context)


def dietetic_space(request):
    """ dietetic_space view """
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

    # call controller_dietetic_space_view method
    # and get context dict
    new_controller = Controller()
    context = new_controller.controller_dietetic_space_view(id_user, old_robot_question,
                                                            data_weight_user, user_answer,
                                                            weekly_weight)

    return render(request, 'dietetic/dietetic_space.html', context)


def my_results(request):
    """ my_results view """
    # get data
    user = get_user_model()
    user = user.objects.get(id=request.user.id)
    final_weight = ProfileUser.objects.values_list("final_weight").get(user=user)[0]
    weighing_date = ResultsUser.objects.values_list("weighing_date")
    weight = ResultsUser.objects.values_list("weight")
    starting_date = weighing_date.filter(user=user).order_by("weighing_date").first()[0]
    last_date = weighing_date.filter(user=user).order_by("weighing_date").last()[0]
    starting_weight = weight.filter(user=user).order_by("weighing_date").first()[0]
    last_weight = weight.filter(user=user).order_by("weighing_date").last()[0]
    total_goal = float(starting_weight - final_weight)

    # get return Calculation class
    new_calculation = Calculation()
    list_data = new_calculation.create_results_data_list(user)
    lost_percentage = new_calculation.percentage_lost_weight(user)
    average_lost_weight = new_calculation.average_weight_loss(user)
    lost_weight = round(starting_weight - last_weight, 1)

    # return list_data (user's results)
    # to the graphic of the results page
    get_data = request.GET.get("get_data", "False")
    if get_data == "True":
        return JsonResponse(list_data, safe=False)

    # if display_info == True
    # display the graphic
    # in the results page
    display_info = False
    if starting_date != last_date:
        display_info = True

    # create a context
    context = {"starting_date": starting_date,
               "starting_weight": new_calculation.delete_o(starting_weight),
               "total_goal": new_calculation.delete_o(total_goal),
               "lost_percentage": lost_percentage,
               "average_lost_weight": new_calculation.delete_o(average_lost_weight),
               "display_info": display_info,
               "final_weight": new_calculation.delete_o(final_weight),
               "lost_weight": new_calculation.delete_o(lost_weight)}

    return render(request, 'dietetic/my_results.html', context)


def program(request):
    """ program view """
    context = {}

    return render(request, 'dietetic/program.html', context)
