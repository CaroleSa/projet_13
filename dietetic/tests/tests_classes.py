#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from django.test import TestCase
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.controller import Controller
from dietetic.models import DiscussionSpace, RobotQuestion
from account.models import ProfileUser, ResultsUser, IdentityUser
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import calendar
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
'fr_FR'


class TestsReturnWeightAdvicesGoal(TestCase):
    """ TestsReturnWeightAdvicesGoal class """

    def setUp(self):
        self.new_weight_advice_goal = WeightAdviceGoal()

    def test_return_goal_under_cruising_weight(self):
        """
        test goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 51}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        actual_weight = data_weight_user["actual_weight"]
        weight_goal = data_weight_user["weight_goal"]
        goal = actual_weight - weight_goal

        self.assertEqual(return_goal, goal)

    def test_return_advice_under_cruising_weight(self):
        """
        test advice returned if the user's weight goal
         is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 51}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                 "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                 "aille en dessous de ce poids. Je tiens donc à te préciser qu'il est" \
                 "possible que tu n'arrives pas à le maintenir sur la durée." \
                 "Je note tout de même cet objectif."

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_under_cruising_weight(self):
        """
        test weight goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 51}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        weight_goal = data_weight_user["weight_goal"]

        self.assertEqual(return_goal, weight_goal)

    def test_return_goal_actual_weight_is_too_low(self):
        """
        test goal returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        user_goal = "impossible"

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_actual_weight_is_too_low(self):
        """
        test advice returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids."

        self.assertEqual(advice, text)

    def test_return_goal_weight_actual_weight_is_too_low(self):
        """
        test goal weight returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        goal_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertEqual(goal_weight, False)

    def test_return_goal_goal_weight_is_too_low(self):
        """
        test goal returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        height = data_weight_user["height"]
        actual_weight = data_weight_user["actual_weight"]
        height_min = round(18.5*(height * height), 1)
        goal = actual_weight - height_min

        self.assertEqual(return_goal, goal)

    def test_return_advice_goal_weight_is_too_low(self):
        """
        test advice returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        height = data_weight_user["height"]
        height_min = round(18.5*(height * height), 1)
        advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                 "aller en dessous de "+str(height_min)+" kg. " \
                 "C'est donc l'objectif que nous allons fixer !"

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_is_too_low(self):
        """
        test goal weight returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]
        height = data_weight_user["height"]
        height_min = round(18.5 * (height * height), 1)

        self.assertEqual(return_goal, height_min)

    def test_return_goal_goal_weight_ok(self):
        """
        test goal returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 55}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        actual_weight = data_weight_user["actual_weight"]
        weight_goal = data_weight_user["weight_goal"]
        goal = actual_weight - weight_goal

        self.assertEqual(return_goal, goal)

    def test_return_advice_goal_weight_ok(self):
        """
        test advice returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 55}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        actual_weight = data_weight_user["actual_weight"]
        weight_goal = data_weight_user["weight_goal"]
        user_goal = float(actual_weight - weight_goal)
        advice = "Alors c'est parti ! Partons sur un objectif de - " \
                 + str(user_goal) + " kg. "

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_ok(self):
        """
        test goal weight returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 55}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        weight_goal = data_weight_user["weight_goal"]

        self.assertEqual(return_goal, weight_goal)


class TestsReturnQuestionsList(TestCase):
    """ TestsReturnQuestionsList class """

    def setUp(self):
        self.new_questions_list = QuestionsList()

    def test_return_questions_list(self):
        """
        test the return of the method :
        list that contains the id questions
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
        for id in id_question_list:
            question = RobotQuestion.objects.get(id=id)
            type = question.robot_question_type.type
            if type == "start":
                id_question_by_type_list.append(id)

        return_list = self.new_questions_list.create_questions_id_list()

        self.assertEqual(id_question_by_type_list, return_list)


class TestsController(TestCase):
    """ TestsController class """

    def setUp(self):
        self.new_controller = Controller()

        # create user account, and add user's data
        self.id_user = 200
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        IdentityUser.objects.create_user(id=self.id_user, username=username2, email=email2, password=password2)
        id = IdentityUser.objects.get(id=self.id_user)
        ProfileUser.objects.create(user=id, starting_weight=60,
                                   actual_goal_weight=5, final_weight=50)
        ResultsUser.objects.create(user=id, weight=60)



    def test(self):
        pass
