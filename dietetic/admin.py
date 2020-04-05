#! /usr/bin/env python3
# coding: UTF-8

""" Admin dietetic app """

# imports
from django.contrib import admin
from .models import RobotQuestionType, RobotAdviceType, RobotQuestion, \
    RobotAdvices, UserAnswer, DiscussionSpace


models_list = {RobotQuestionType: ["type"],
               RobotAdviceType: ["type"],
               RobotQuestion: [["robot_question_type", "text"], ["robot_question_type"]],
               RobotAdvices: [["robot_advice_type", "text"], ["robot_advice_type"]],
               UserAnswer: ["text"],
               DiscussionSpace: [["id", "robot_question", "user_answer",
                                 "robot_answer", "robot_advices"],
                                 ["robot_question"]]}

for model, fields in models_list.items():

    class DieteticAdmin(admin.ModelAdmin):
        """ DieteticAdmin class """
        if len(fields) == 2:
            if type(fields[1]) == list:
                list_display = fields[0]
                list_filter = fields[1]
            else:
                list_display = fields
        else:
            list_display = fields

    admin.site.register(model, DieteticAdmin)
