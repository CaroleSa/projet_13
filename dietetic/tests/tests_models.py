#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from dietetic.models import RobotQuestion, RobotQuestionType, RobotAdviceType, \
    UserAnswer, RobotAdvices, DiscussionSpace
from django.db.utils import IntegrityError


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    def setUp(self):
        # get custom user model
        self.user = get_user_model()

        # delete all data in database
        models_list = [RobotQuestion, RobotQuestionType, RobotAdviceType,
                      UserAnswer, RobotAdvices, DiscussionSpace, self.user]
        for table in models_list:
            table.objects.all().delete()

        # create user account
        self.username2 = 'pseudo2'
        self.email2 = 'pseudo2@tests.com'
        self.password2 = 'password2'
        self.user.objects.create_user(username=self.username2, email=self.email2,
                                      password=self.password2)
        self.user_created = self.user.objects.get(username=self.username2)

        # create robot question type
        self.question_type = "Questions type"
        self.id_question_type = 1
        try:
            RobotQuestionType.objects.create(id=self.id_question_type, type=self.question_type)
        except IntegrityError:
            pass
        self.robot_question_type = RobotQuestionType.objects.get(type=self.question_type)

        # create robot question
        self.question = "Question"
        self.id_question_robot = 1
        try:
            RobotQuestion.objects.create(id=self.id_question_robot, text=self.question,
                                         robot_question_type=self.robot_question_type)
        except IntegrityError:
            pass
        self.robot_question = RobotQuestion.objects.get(text=self.question)

        # create robot advice type
        self.advice_type = "Recette"
        self.id_advice_type = 1
        try:
            RobotAdviceType.objects.create(id=self.id_advice_type, type=self.advice_type)
        except IntegrityError:
            pass
        self.robot_advice_type = RobotAdviceType.objects.get(type=self.advice_type)

        # create user answer
        self.answer = "Non"
        self.id_user_answer = 1
        try:
            UserAnswer.objects.create(id=self.id_user_answer, text=self.answer)
        except IntegrityError:
            pass
        self.user_answer = UserAnswer.objects.get(text=self.answer)

        # create robot advices
        self.advice = "is a robot advice"
        self.id_robot_advice = 1
        try:
            RobotAdvices.objects.create(id=self.id_robot_advice, text=self.advice, robot_advice_type=self.robot_advice_type)
        except IntegrityError:
            pass
        self.robot_advices = RobotAdvices.objects.get(text=self.advice)

    def test_add_robot_question(self):
        """ Test create robot question """
        question = "Question test"
        try:
            RobotQuestion.objects.create(text=question, robot_question_type=self.robot_question_type)
        except IntegrityError:
            pass
        question_exists = RobotQuestion.objects.get(text=question)
        self.assertTrue(question_exists)

    def test_add_robot_question_type(self):
        """ Test create robot question type """
        type = "Start questions"
        try:
            RobotQuestionType.objects.create(type=type)
        except IntegrityError:
            pass
        type_exists = RobotQuestionType.objects.get(type=type)
        self.assertTrue(type_exists)

    def test_add_robot_advice_type(self):
        """ Test create robot advice type """
        type = "Challenge"
        try:
            RobotAdviceType.objects.create(type=type)
        except IntegrityError:
            pass
        type_exists = RobotAdviceType.objects.get(type=type)
        self.assertTrue(type_exists)

    def test_add_user_answer(self):
        """ Test add user answer """
        answer = "Oui"
        try:
            UserAnswer.objects.create(text=answer)
        except IntegrityError:
            pass
        answer_exists = UserAnswer.objects.get(text=answer)
        self.assertTrue(answer_exists)

    def test_add_robot_advices(self):
        """ Test add robot advices """
        advice = "is an advice test"
        try:
            RobotAdvices.objects.create(text=advice, robot_advice_type=self.robot_advice_type)
        except IntegrityError:
            pass
        advice_exists = RobotAdvices.objects.get(text=advice)
        self.assertTrue(advice_exists)

    def test_add_discussion_space(self):
        """ Test add discussion space """
        answer = "is an answer test"
        try:
            DiscussionSpace.objects.create(robot_answer=answer, robot_question=self.robot_question,
                                           user_answer=self.user_answer, robot_advices=self.robot_advices)
        except IntegrityError:
            pass
        discussion_exists = DiscussionSpace.objects.get(robot_answer=answer)
        self.assertTrue(discussion_exists)

    def test_get_question_type(self):
        """ Test get value question type """
        data = RobotQuestionType.objects.values_list('type').get(id=self.id_question_type)
        self.assertEqual(data[0], self.question_type)

    def test_get_advice_type(self):
        """ Test get value advice type """
        data = RobotAdviceType.objects.values_list('type').get(id=self.id_advice_type)
        self.assertEqual(data[0], self.advice_type)

    def test_get_robot_question(self):
        """ Test get robot question value """
        data = RobotQuestion.objects.values_list('text').get(id=self.id_question_robot)
        self.assertEqual(data[0], self.question)

    def test_get_user_answer(self):
        """ Test get user answer value """
        data = UserAnswer.objects.values_list('text').get(id=self.id_user_answer)
        self.assertEqual(data[0], self.answer)

    def test_get_robot_advices(self):
        """ Test get robot advices value """
        data = RobotAdvices.objects.values_list('text').get(id=self.id_robot_advice)
        self.assertEqual(data[0], self.advice)

    #def test_add_advices_to_user(self):
        #""" Test add advices to user """
        ### DON'T WORKS !!!
        #self.robot_advices.advices_to_user.add(self.user_created)
