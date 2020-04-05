#! /usr/bin/env python3
# coding: UTF-8

""" Admin account app """

# imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import AdvicesToUser, StatusUser, \
    HistoryUser, ProfileUser, ResultsUser


user_model = get_user_model()
@admin.register(user_model)
class CustomUserAdmin(admin.ModelAdmin):
    """ CustomUserAdmin class """
    list_display = ["username", "email", "is_staff", "is_superuser"]
    list_filter = ["is_staff", "is_superuser"]


models_list = {AdvicesToUser: [["user", "advice"], ["user"]],
               StatusUser: ["user", "is_active"],
               HistoryUser: [["user", "date_joined", "start_questionnaire_completed"],
                             ["start_questionnaire_completed"]],
               ProfileUser: ["user", "starting_weight", "actual_goal_weight", "final_weight"],
               ResultsUser: [["user", "weighing_date", "weight"], ["user"]]}

for model, fields in models_list.items():

    class AccountAdmin(admin.ModelAdmin):
        """ AccountAdmin class """
        if len(fields) == 2:
            if type(fields[1]) == list:
                list_display = fields[0]
                list_filter = fields[1]
            else:
                list_display = fields
        else:
            list_display = fields


    admin.site.register(model, AccountAdmin)
