#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from django.test import TestCase
from django.contrib.auth import get_user_model
from dietetic.models import RobotQuestion, RobotQuestionType, RobotAdviceType, \
    UserAnswer, RobotAdvices, DiscussionSpace
from django.db.utils import IntegrityError


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    fixtures = ["data.json"]

    def setUp(self):
        # create user account
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        user = get_user_model()
        user.objects.create_user(username=username2, email=email2, password=password2)
        self.user_created = user.objects.get(username=username2)

        # get data
        self.robot_question_type = RobotQuestionType.objects.first()
        self.robot_question = RobotQuestion.objects.first()
        self.robot_advice_type = RobotAdviceType.objects.first()
        self.user_answer = UserAnswer.objects.last()
        self.robot_advices = RobotAdvices.objects.first()

    def test_add_get_robot_question(self):
        """ Test create robot question and get values """
        question = "Question test"
        RobotQuestion.objects.create(text=question, robot_question_type=self.robot_question_type)
        id = RobotQuestion.objects.values_list("id").get(text=question)[0]
        data = RobotQuestion.objects.values_list("text").get(id=id)
        self.assertEqual(data[0], question)

    def test_add_get_robot_question_type(self):
        """ Test create robot question type and get values """
        type = "Type question test"
        RobotQuestionType.objects.create(type=type)
        id = RobotQuestionType.objects.values_list("id").get(type=type)[0]
        data = RobotQuestionType.objects.values_list("type").get(id=id)
        self.assertEqual(data[0], type)

    def test_add_get_robot_advice_type(self):
        """ Test create robot advice type and get values """
        type = "Type conseil test"
        RobotAdviceType.objects.create(type=type)
        id = RobotAdviceType.objects.values_list("id").get(type=type)[0]
        data = RobotAdviceType.objects.values_list("type").get(id=id)
        self.assertEqual(data[0], type)

    def test_add_get_user_answer(self):
        """ Test add user answer and get values """
        answer = "Réponse utilisateur test"
        UserAnswer.objects.create(text=answer)
        id = UserAnswer.objects.values_list("id").get(text=answer)[0]
        data = UserAnswer.objects.values_list("text").get(id=id)
        self.assertEqual(data[0], answer)

    def test_add_get_robot_advices(self):
        """ Test add robot advices and get values """
        advice = "Conseil test"
        RobotAdvices.objects.create(text=advice, robot_advice_type=self.robot_advice_type)
        id = RobotAdvices.objects.values_list("id").get(text=advice)[0]
        data = RobotAdvices.objects.values_list("text").get(id=id)
        self.assertEqual(data[0], advice)

    def test_add_get_discussion_space(self):
        """ Test add discussion space and get values """
        answer = "Réponse du robot test"
        DiscussionSpace.objects.create(robot_answer=answer, robot_question=self.robot_question,
                                       user_answer=self.user_answer, robot_advices=self.robot_advices)
        data = DiscussionSpace.objects.values_list("robot_answer").filter(robot_question=self.robot_question)\
            .get(user_answer=self.user_answer)

        self.assertEqual(data[0], answer)

    def test_add_advices_to_user(self):
        """### DON'T WORKS !!!
        username2 = 'pseudo2'
        email2 = 'pseudo2@tesgdfgts.com'
        password2 = 'password2'
        user = get_user_model()
        user = user.objects.create_user(username=username2, email=email2, password=password2)
        advices = RobotAdvices.objects.get(id=3)
        user.advices_to_user.add(advices)"""
