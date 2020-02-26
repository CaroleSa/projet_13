#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model
from dietetic.models import RobotQuestion, RobotQuestionType, RobotAdviceType, \
    UserAnswer, RobotAdvices, DiscussionSpace
from django.db.utils import IntegrityError


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    def setUp(self):
        # get custom user model
        user = get_user_model()

        # delete all data in database
        models_list = [RobotQuestion, RobotQuestionType, RobotAdviceType,
                       UserAnswer, RobotAdvices, DiscussionSpace, user]
        for table in models_list:
            table.objects.all().delete()

        # create user account
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        user.objects.create_user(username=username2, email=email2, password=password2)
        self.user_created = user.objects.get(username=username2)

        # create robot question type
        question_type = "Questions type"
        id_question_type = 1
        try:
            RobotQuestionType.objects.create(id=id_question_type, type=question_type)
        except IntegrityError:
            pass
        self.robot_question_type = RobotQuestionType.objects.get(type=question_type)

        # create robot question
        question = "Question"
        id_question_robot = 1
        try:
            RobotQuestion.objects.create(id=id_question_robot, text=question,
                                         robot_question_type=self.robot_question_type)
        except IntegrityError:
            pass
        self.robot_question = RobotQuestion.objects.get(text=question)

        # create robot advice type
        advice_type = "Recette"
        id_advice_type = 1
        try:
            RobotAdviceType.objects.create(id=id_advice_type, type=advice_type)
        except IntegrityError:
            pass
        self.robot_advice_type = RobotAdviceType.objects.get(type=advice_type)

        # create user answer
        answer = "Non"
        id_user_answer = 1
        try:
            UserAnswer.objects.create(id=id_user_answer, text=answer)
        except IntegrityError:
            pass
        self.user_answer = UserAnswer.objects.get(text=answer)

        # create robot advices
        advice = "is a robot advice"
        id_robot_advice = 1
        try:
            RobotAdvices.objects.create(id=id_robot_advice, text=advice, robot_advice_type=self.robot_advice_type)
        except IntegrityError:
            pass
        self.robot_advices = RobotAdvices.objects.get(text=advice)

    def test_add_get_robot_question(self):
        """ Test create robot question and get values """
        question = "Question test"
        question_id = 2
        try:
            RobotQuestion.objects.create(id=question_id, text=question, robot_question_type=self.robot_question_type)
        except IntegrityError:
            pass
        data = RobotQuestion.objects.values_list("text").get(id=question_id)
        self.assertEqual(data[0], question)

    def test_add_get_robot_question_type(self):
        """ Test create robot question type and get values """
        type = "Start questions"
        id_type = 2
        try:
            RobotQuestionType.objects.create(id=id_type, type=type)
        except IntegrityError:
            pass
        data = RobotQuestionType.objects.values_list("type").get(id=id_type)
        self.assertEqual(data[0], type)

    def test_add_get_robot_advice_type(self):
        """ Test create robot advice type and get values """
        type = "Challenge"
        id_type = 2
        try:
            RobotAdviceType.objects.create(id=id_type, type=type)
        except IntegrityError:
            pass
        data = RobotAdviceType.objects.values_list("type").get(id=id_type)
        self.assertEqual(data[0], type)

    def test_add_get_user_answer(self):
        """ Test add user answer and get values """
        answer = "Oui"
        id_answer = 2
        try:
            UserAnswer.objects.create(id=id_answer, text=answer)
        except IntegrityError:
            pass
        data = UserAnswer.objects.values_list("text").get(id=id_answer)
        self.assertEqual(data[0], answer)

    def test_add_get_robot_advices(self):
        """ Test add robot advices and get values """
        advice = "is an advice test"
        id_advice = 2
        try:
            RobotAdvices.objects.create(id=id_advice, text=advice, robot_advice_type=self.robot_advice_type)
        except IntegrityError:
            pass
        data = RobotAdvices.objects.values_list("text").get(id=id_advice)
        self.assertEqual(data[0], advice)

    def test_add_get_discussion_space(self):
        """ Test add discussion space and get values """
        answer = "is an answer test"
        try:
            DiscussionSpace.objects.create(robot_answer=answer, robot_question=self.robot_question,
                                           user_answer=self.user_answer, robot_advices=self.robot_advices)
        except IntegrityError:
            pass
        data = DiscussionSpace.objects.values_list("robot_answer").get(robot_advices=self.robot_advices)
        self.assertEqual(data[0], answer)

    def test_add_advices_to_user(self):
        """ Test add advices to user """
        ### DON'T WORKS !!!
        self.robot_advices.advices_to_user.add(self.user_created)
