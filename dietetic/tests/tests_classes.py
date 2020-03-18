#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from django.test import TestCase
from django.contrib.auth import get_user_model
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.calculation import Calculation
from dietetic.classes.controller import Controller
from dietetic.models import DiscussionSpace, RobotQuestion
from account.models import ProfileUser, ResultsUser, IdentityUser, StatusUser, HistoryUser
from datetime import date, timedelta
import calendar
from django.db import connection
from django.db.utils import IntegrityError
from psycopg2.errors import UniqueViolation

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
'fr_FR'


class TestsReturnWeightAdvicesGoal(TestCase):
    """ TestsReturnWeightAdvicesGoal class """

    def setUp(self):
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.new_calculation = Calculation()

    def test_return_goal_under_cruising_weight(self):
        """
        test goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "51"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        actual_weight = round(float(data_weight_user["actual_weight"]), 1)
        weight_goal = round(float(data_weight_user["weight_goal"]), 1)
        goal = actual_weight - weight_goal

        self.assertEqual(return_goal, goal)

    def test_return_advice_under_cruising_weight(self):
        """
        test advice returned if the user's weight goal
         is under to this cruising weight
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "51"}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                 "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                 "aille en dessous de ce poids. Je tiens donc à te préciser qu'il est" \
                 "possible que tu n'arrives pas à le maintenir sur la durée." \
                 "Je note tout de même cet objectif. "

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_under_cruising_weight(self):
        """
        test weight goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "51"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        weight_goal = round(float(data_weight_user["weight_goal"]), 1)

        self.assertEqual(return_goal, weight_goal)

    def test_return_goal_actual_weight_is_too_low(self):
        """
        test goal returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        user_goal = "impossible"

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_actual_weight_is_too_low(self):
        """
        test advice returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids. "

        self.assertEqual(advice, text)

    def test_return_goal_weight_actual_weight_is_too_low(self):
        """
        test goal weight returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        goal_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertEqual(goal_weight, False)

    def test_return_goal_goal_weight_is_too_low(self):
        """
        test goal returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        height = data_weight_user["height"]
        height = float(height.replace(",", "."))
        actual_weight = round(float(data_weight_user["actual_weight"]), 1)
        height_min = round(18.5*(height * height), 1)
        goal = actual_weight - height_min

        self.assertEqual(return_goal, goal)

    def test_return_advice_goal_weight_is_too_low(self):
        """
        test advice returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        height = data_weight_user["height"]
        height = float(height.replace(",", "."))
        height_min = round(18.5*(height * height), 1)
        height_min = self.new_calculation.delete_o(height_min)
        advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                 "aller en dessous de "+str(height_min)+" kg. " \
                 "C'est donc l'objectif que nous allons fixer ! "

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_is_too_low(self):
        """
        test goal weight returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]
        height = data_weight_user["height"]
        height = float(height.replace(",", "."))
        height_min = round(18.5 * (height * height), 1)

        self.assertEqual(return_goal, height_min)

    def test_return_goal_goal_weight_ok(self):
        """
        test goal returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        actual_weight = round(float(data_weight_user["actual_weight"]), 1)
        weight_goal = round(float(data_weight_user["weight_goal"]), 1)
        goal = actual_weight - weight_goal

        self.assertEqual(return_goal, goal)

    def test_return_advice_goal_weight_ok(self):
        """
        test advice returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        actual_weight = round(float(data_weight_user["actual_weight"]), 1)
        weight_goal = round(float(data_weight_user["weight_goal"]), 1)
        user_goal = self.new_calculation.delete_o(float(actual_weight - weight_goal))
        advice = "Alors c'est parti ! Partons sur un objectif de - " \
                 + str(user_goal) + " kg. "

        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_ok(self):
        """
        test goal weight returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        weight_goal = round(float(data_weight_user["weight_goal"]), 1)

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
            question_type = question.robot_question_type.type
            if question_type == "start":
                id_question_by_type_list.append(id)

        return_list = self.new_questions_list.create_questions_id_list()

        self.assertEqual(id_question_by_type_list, return_list)
        self.assertEqual(list, type(return_list))


class TestsCalculation(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.user = get_user_model()
        self.cursor = connection.cursor()
        self.new_calculation = Calculation()

    def create_user(self):
        """
        create a user
        """
        dict_data_user = {"id_email": "carole5@test.fr", "id_password": "00000000"}
        id_user = 1
        try:
            user_created = self.user.objects.create_user(id=id_user, username="pseudo",
                                                         email=dict_data_user.get('id_email'),
                                                         password=dict_data_user.get('id_password'))
            HistoryUser.objects.create(user=user_created)
            StatusUser.objects.create(user=user_created)
            ProfileUser.objects.create(user=user_created, starting_weight=100,
                                       actual_goal_weight=50, final_weight=50)
            one_week_before = date.today() - timedelta(days=7)
            ResultsUser.objects.create(user=user_created, weighing_date=one_week_before, weight=100)
            ResultsUser.objects.create(user=user_created, weighing_date=date.today(), weight=95)
            user = HistoryUser.objects.get(user=user_created)
            user.start_questionnaire_completed = True
            user.save()
            list_advice_id = [1, 4, 8, 10]
            for id_advice in list_advice_id:
                self.cursor.execute("INSERT INTO account_identityuser_advices_to_user "
                                    "(identityuser_id, robotadvices_id) "
                                    "VALUES ({}, {})".format(id_user, id_advice))
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created

    def test_create_results_data_list(self):
        user_created = self.create_user()
        starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).first()[0]
        results_weight_data = ResultsUser.objects.values_list("weight").filter(user=user_created).order_by("weighing_date")
        results_date_data = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).order_by("weighing_date")

        list_data = [['Semaine', 'Poids']]
        for date, weight in zip(results_date_data, results_weight_data):
            delta = date[0] - starting_date
            number_of_weeks = round(delta.days / 7, 0)
            list_date_weight = [number_of_weeks, float(weight[0])]
            list_data.append(list_date_weight)

        list_return = self.new_calculation.create_results_data_list(user_created)

        self.assertEqual(list_data, list_return)
        self.assertEqual(list, type(list_return))
        for elt in list_return:
            self.assertEqual(list, type(elt))
            self.assertEqual(2, len(elt))

    def test_percentage_lost_weight(self):
        user_created = self.create_user()
        starting_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).first()[0]
        last_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).last()[0]
        final_weight = ProfileUser.objects.values_list("final_weight").get(user=user_created)[0]
        total_lost_weight = float(starting_weight - last_weight)
        total_goal = float(starting_weight - final_weight)
        lost_percentage = round(int((total_lost_weight * 100) / total_goal), 0)

        percentage_return = self.new_calculation.percentage_lost_weight(user_created)

        self.assertEqual(percentage_return, lost_percentage)
        self.assertEqual(type(percentage_return), int)

    def test_average_weight_loss(self):
        user_created = self.create_user()
        starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).first()[0]
        last_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).last()[0]
        starting_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).first()[0]
        last_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).last()[0]
        total_lost_weight = float(starting_weight - last_weight)
        delta = last_date - starting_date
        number_of_weeks = delta.days / 7
        try:
            average_lost_weight = round(total_lost_weight / number_of_weeks, 1)
        except ZeroDivisionError:
            average_lost_weight = 0

        average_return = self.new_calculation.average_weight_loss(user_created)

        self.assertEqual(average_return, average_lost_weight)
        self.assertEqual(type(average_return), float)

    def test_delete_o(self):
        number = 6.0
        number_return = self.new_calculation.delete_o(number)
        self.assertEqual(number_return, 6)
        self.assertNotEqual(type(number), int)
        self.assertEqual(type(number_return), int)

        number = 10.565
        number_return = self.new_calculation.delete_o(number)
        self.assertEqual(number_return, 10.565)
        self.assertEqual(type(number_return), float)

        number = 10
        number_return = self.new_calculation.delete_o(number)
        self.assertEqual(number_return, 10)
        self.assertEqual(type(number_return), int)


class TestsController(TestCase):
    """ TestsController class """

    def setUp(self):
        self.new_controller = Controller()
        self.cursor = connection.cursor()
        self.user = get_user_model()

        # create user account, and add user's data
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        self.user_created = self.user.objects.create_user(id=1, username=username2, email=email2, password=password2)
        HistoryUser.objects.create(user=self.user_created)
        StatusUser.objects.create(user=self.user_created)

        ProfileUser.objects.create(user=self.user_created, starting_weight=60,
                                   actual_goal_weight=5, final_weight=50)
        ResultsUser.objects.create(user=self.user_created, weight=60)
        user = HistoryUser.objects.get(user=self.user_created)
        user.start_questionnaire_completed = True
        user.save()

    def test_parser_weight(self):
        data_weight_user = {"height": 1.60, "actual_weight": 100,
                            "cruising_weight": 50, "weight_goal": 50}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        self.assertTrue(return_validate)
        self.assertEqual(return_context, {})

        data_weight_user = {"height": 1.60, "actual_weight": 50,
                            "cruising_weight": 50, "weight_goal": 60}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        text = "Ton objectif doit être inférieur à ton poids actuel."
        self.assertFalse(return_validate)
        self.assertEqual(return_context, {"error_message": text})
        self.assertEqual(type(return_context), dict)

    def test_return_text_congratulations_restart_program(self):
        pseudo = self.user_created.username
        text = "Félicitation {} ! Tu as atteints ton objectif !".format(pseudo)

        data_profile = ProfileUser.objects.all().count()
        data_results = ResultsUser.objects.all().count()

        user = HistoryUser.objects.get(user=self.user_created)
        before_method = user.start_questionnaire_completed

        return_text = self.new_controller.return_text_congratulations_restart_program(self.user_created.id)

        after_method = user.start_questionnaire_completed

        #self.assertFalse(after_method)
        #self.assertNotEqual(before_method, after_method)
        self.assertEqual(type(return_text), str)
        self.assertEqual(return_text, text)
        #self.assertEqual(data_profile, 0)
        #self.assertEqual(data_results, 0)

    def test_add_advices_to_user(self):
        # check the advices number before method == 0
        # return_text = self.new_controller.add_advices_to_user(self.id_user)
        # check the advices number after method == 10 ???
        pass