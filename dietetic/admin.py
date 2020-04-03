#! /usr/bin/env python3
# coding: UTF-8

""" Admin dietetic app """

# imports
from django.contrib import admin
from .models import RobotQuestionType, RobotAdviceType, RobotQuestion, \
    RobotAdvices, UserAnswer, DiscussionSpace


models_list = {RobotQuestionType: ["type"],
               RobotAdviceType: ["type"],
               RobotQuestion: ["robot_question_type", "text"],
               RobotAdvices: ["robot_advice_type", "text"],
               UserAnswer: ["text"],
               DiscussionSpace: ["id", "robot_question", "user_answer",
                                 "robot_answer", "robot_advices"]}

for model, fields in models_list.items():

    class ProductAdmin(admin.ModelAdmin):
        list_display = fields

    admin.site.register(model, ProductAdmin)
