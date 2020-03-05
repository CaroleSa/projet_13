#! /usr/bin/env python3
# coding: UTF-8

""" QuestionsList class """

# Imports
from ..models import DiscussionSpace


class QuestionsList:

    def create_questions_id_list(self):
        """ create a list : robot questions
        by order discussion_space id """

        data = DiscussionSpace.objects.values_list("robot_question").order_by("id")
        list_data = []
        for elt in data:
            list_data.append(elt[0])
        new_list = []
        for i in list_data:
            if i not in new_list:
                new_list.append(i)

        return new_list
