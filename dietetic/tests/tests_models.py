#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from dietetic.models import RobotQuestion, RobotQuestionType
from django.db.utils import IntegrityError


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    def setUp(self):
        # get custom user model
        self.user = get_user_model()

        # create user account
        self.username2 = 'pseudo2'
        self.email2 = 'pseudo2@tests.com'
        self.password2 = 'password2'
        self.id_user2 = 2
        self.user.objects.create_user(id=self.id_user2, username=self.username2, email=self.email2,
                                      password=self.password2)

        # create robot question type
        type = "Questions type"
        try:
            RobotQuestionType.objects.create(type=type)
        except IntegrityError:
            pass
        self.robot_question_type = RobotQuestionType.objects.get(type=type)

    def test_add_question_robot(self):
        """ Test create robot question """
        question = "Question test"
        try:
            RobotQuestion.objects.create(text=question, robot_question_type=self.robot_question_type)
        except IntegrityError:
            pass
        question_exists = RobotQuestion.objects.get(text=question)
        self.assertTrue(question_exists)

    def test_add_question_type(self):
        """ Test create robot question type """
        type = "Start questions"
        try:
            RobotQuestionType.objects.create(type=type)
        except IntegrityError:
            pass
        type_exists = RobotQuestionType.objects.get(type=type)
        self.assertTrue(type_exists)
