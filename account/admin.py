#! /usr/bin/env python3
# coding: UTF-8

""" Admin account app """

# imports
from django.contrib import admin
from account.models import IdentityUser, AdvicesToUser, StatusUser, \
    HistoryUser, ProfileUser, ResultsUser


@admin.register(IdentityUser)
class CustomUserAdmin(admin.ModelAdmin):
    """ CustomUserAdmin class """
    pass


models_list = {AdvicesToUser: ["user", "advice"],
               StatusUser: ["user", "is_active"],
               HistoryUser: ["user", "date_joined", "start_questionnaire_completed"],
               ProfileUser: ["user", "starting_weight", "actual_goal_weight", "final_weight"],
               ResultsUser: ["user", "weighing_date", "weight"]}

for model, fields in models_list.items():

    class ProductAdmin(admin.ModelAdmin):
        """ ProductAdmin class """
        list_display = fields

    admin.site.register(model, ProductAdmin)
