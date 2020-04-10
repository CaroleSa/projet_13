#! /usr/bin/env python3
# coding: UTF-8

""" QuestionsList class """

# Imports
from dietetic.models import DiscussionSpace, RobotQuestion
# pylint: disable=no-member


class QuestionsList:
    """ QuestionsList class """

    @classmethod
    def create_questions_id_list(cls):
        """
        create a list : robot questions
        by order discussion_space id
        """
        data = DiscussionSpace.objects.values_list("robot_question").order_by("id")
        list_data = []
        for elt in data:
            list_data.append(elt[0])
        id_question_list = []
        for i in list_data:
            if i not in id_question_list:
                id_question_list.append(i)

        id_question_by_type_list = []
        for id_question in id_question_list:
            question = RobotQuestion.objects.get(id=id_question)
            question_type = question.robot_question_type.type
            if question_type == "start":
                id_question_by_type_list.append(id_question)

        return id_question_by_type_list
