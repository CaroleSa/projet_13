#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import connection
from dietetic.models import RobotQuestion, RobotQuestionType, RobotAdviceType, \
    UserAnswer, RobotAdvices, DiscussionSpace
# pylint: disable=no-member


class TestsModels(TestCase):
    """ TestsModels class """

    fixtures = ["data.json"]

    def setUp(self):
        # create user account
        self.id_user = 1
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        user = get_user_model()
        user.objects.create_user(id=1, username=username2, email=email2,
                                 password=password2)
        self.user_created = user.objects.get(username=username2)

        # get data
        self.robot_question_type = RobotQuestionType.objects.first()
        self.robot_question = RobotQuestion.objects.first()
        self.robot_advice_type = RobotAdviceType.objects.first()
        self.user_answer = UserAnswer.objects.last()
        self.robot_advices = RobotAdvices.objects.first()

        # create robot advice
        advice = "Conseil test2"
        self.advice_id = RobotAdvices.objects.values_list("id").last()[0] + 1
        RobotAdvices.objects.create(id=self.advice_id, text=advice,
                                    robot_advice_type=self.robot_advice_type)

    def test_add_get_robot_question(self):
        """
        Test create robot question
        and get values
        """
        question = "Question test"
        RobotQuestion.objects.create(text=question,
                                     robot_question_type=self.robot_question_type)
        id_question = RobotQuestion.objects.values_list("id").get(text=question)[0]
        data = RobotQuestion.objects.values_list("text").get(id=id_question)
        self.assertEqual(data[0], question)

    def test_add_get_robot_question_type(self):
        """
        Test create robot question
        type and get values
        """
        type_question = "Type question test"
        RobotQuestionType.objects.create(type=type_question)
        id_question = RobotQuestionType.objects.values_list("id").get(type=type_question)[0]
        data = RobotQuestionType.objects.values_list("type").get(id=id_question)
        self.assertEqual(data[0], type_question)

    def test_add_get_robot_advice_type(self):
        """
        Test create robot advice
        type and get values
        """
        type_advice = "Type conseil test"
        RobotAdviceType.objects.create(type=type_advice)
        id_advice = RobotAdviceType.objects.values_list("id").get(type=type_advice)[0]
        data = RobotAdviceType.objects.values_list("type").get(id=id_advice)
        self.assertEqual(data[0], type_advice)

    def test_add_get_user_answer(self):
        """
        Test add user answer
        and get values
        """
        answer = "Réponse utilisateur test"
        UserAnswer.objects.create(text=answer)
        id_answer = UserAnswer.objects.values_list("id").get(text=answer)[0]
        data = UserAnswer.objects.values_list("text").get(id=id_answer)
        self.assertEqual(data[0], answer)

    def test_add_get_robot_advices(self):
        """
        Test add robot advices
        and get values
        """
        advice = "Conseil test"
        advice_id = RobotAdvices.objects.values_list("id").last()[0] + 1
        RobotAdvices.objects.create(id=advice_id, text=advice,
                                    robot_advice_type=self.robot_advice_type)
        id_advice = RobotAdvices.objects.values_list("id").get(text=advice)[0]
        data = RobotAdvices.objects.values_list("text").get(id=id_advice)
        self.assertEqual(data[0], advice)

    def test_add_get_discussion_space(self):
        """
        Test add discussion space
        and get values
        """
        answer = "Réponse du robot test"
        DiscussionSpace.objects.create(robot_answer=answer,
                                       robot_question=self.robot_question,
                                       user_answer=self.user_answer,
                                       robot_advices=self.robot_advices)
        data = DiscussionSpace.objects.values_list("robot_answer")\
            .filter(robot_question=self.robot_question).get(user_answer=self.user_answer)

        self.assertEqual(data[0], answer)

    def test_add_get_advices_to_user(self):
        """
        Test add advice
        and get advices to user
        """
        cursor = connection.cursor()
        cursor.execute("INSERT INTO account_identityuser_advices_to_user "
                       "(identityuser_id, robotadvices_id) "
                       "VALUES ({}, {})".format(self.id_user, self.advice_id))
        advice_to_user = self.user_created.advices_to_user.values_list("text")[0]
        advice = RobotAdvices.objects.values_list("text").get(identityuser=self.id_user)
        self.assertEqual(advice_to_user[0], advice[0])
