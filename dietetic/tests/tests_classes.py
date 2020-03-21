#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.calculation import Calculation
from dietetic.classes.controller import Controller
from dietetic.models import DiscussionSpace, RobotQuestion, RobotAdviceType, RobotAdvices, UserAnswer
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

    fixtures = ['data.json']

    def setUp(self):
        self.new_controller = Controller()
        self.new_questions_list = QuestionsList()
        self.cursor = connection.cursor()
        self.user = get_user_model()

        # create user account, and add user's data
        username2 = 'pseudo2'
        email2 = 'pseudo2@tests.com'
        password2 = 'password2'
        self.user_created = self.user.objects.create_user(id=1, username=username2, email=email2, password=password2)
        HistoryUser.objects.create(user=self.user_created)
        StatusUser.objects.create(user=self.user_created)
        self.actual_goal = 10
        ProfileUser.objects.create(user=self.user_created, starting_weight=60,
                                   actual_goal_weight=self.actual_goal, final_weight=50)
        present = datetime.now()
        present_date = present.date()
        weighing_date = present_date - timedelta(days=7)
        ResultsUser.objects.create(user=self.user_created, weighing_date=weighing_date, weight=60)
        user = HistoryUser.objects.get(user=self.user_created)
        user.start_questionnaire_completed = True
        user.save()

    def add_advice_to_user_created(self, user_id, list_advice_id):
        for id_advice in list_advice_id:
            self.cursor.execute("INSERT INTO account_identityuser_advices_to_user "
                                "(identityuser_id, robotadvices_id) "
                                "VALUES ({}, {})".format(user_id, id_advice))

    def test_parser_weight(self):
        data_weight_user = {"height": "1,60", "actual_weight": "100",
                            "cruising_weight": "50", "weight_goal": "50"}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        self.assertTrue(return_validate)
        self.assertEqual(return_context, {})

        data_weight_user = {"height": "1,60", "actual_weight": "50",
                            "cruising_weight": "50", "weight_goal": "60"}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        text = "Ton objectif doit être inférieur à ton poids actuel."
        self.assertFalse(return_validate)
        self.assertEqual(return_context, {"error_message": text})
        self.assertEqual(type(return_context), dict)

    def test_return_text_congratulations_restart_program(self):
        pseudo = self.user_created.username
        text = "Félicitation {} ! Tu as atteints ton objectif !".format(pseudo)
        data_profile_before = ProfileUser.objects.all().count()
        data_results_before = ResultsUser.objects.all().count()
        before_method = HistoryUser.objects.values_list("start_questionnaire_completed").get(user=self.user_created)[0]

        return_text = self.new_controller.return_text_congratulations_restart_program(self.user_created.id)

        after_method = HistoryUser.objects.values_list("start_questionnaire_completed").get(user=self.user_created)[0]
        data_profile_after = ProfileUser.objects.all().count()
        data_results_after = ResultsUser.objects.all().count()

        self.assertFalse(after_method)
        self.assertNotEqual(before_method, after_method)
        self.assertEqual(type(return_text), str)
        self.assertEqual(return_text, text)
        self.assertEqual(data_profile_after, 0)
        self.assertEqual(data_results_after, 0)
        self.assertNotEqual(data_profile_before, data_profile_after)
        self.assertNotEqual(data_results_before, data_results_after)

    def test_add_advices_to_user(self):
        """
        test that the method add
        a new challenges to user
        """
        # count the number of challenges before a call to the method
        user = IdentityUser.objects.get(id=self.user_created.id)
        advice_to_user_before = user.advices_to_user.all().count()

        # call method
        self.new_controller.add_advices_to_user(self.user_created.id)

        # count the number of challenges after a call to the method
        advice_to_user_after = user.advices_to_user.all().count()

        self.assertEqual(advice_to_user_before, 0)
        self.assertNotEqual(advice_to_user_after, 0)
        self.assertNotEqual(advice_to_user_after, advice_to_user_before)

    def test_return_weekly_questions_save_weight(self):
        """
        test the returns of the method
        and check that the weight is save
        """
        # TEST NEW WEIGHT DON'T EXISTS
        # data
        weekly_weight = False
        # call method
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight, self.user_created.id)

        self.assertEqual(context["robot_comment"], "Bonjour ! J'éspère que ta semaine s'est bien passée ? "
                                                   "Que donne ta pesée ce matin ?")
        self.assertTrue(context["robot_weekly_weight"])

        # TEST ADD THE NEW WEIGHT
        # data
        weekly_weight = 58
        # call method, check text returns
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight, self.user_created.id)
        # check the last weight saved
        last_weight = ResultsUser.objects.values_list("weight").filter(user=self.user_created).last()[0]

        self.assertEqual(context["robot_comment"], "J'ai bien pris note de ton poids, "
                                                   "tu trouveras un récapitulatif dans "
                                                   "l'onglet résultats.")
        self.assertEqual(last_weight, weekly_weight)

        # TEST AFTER ADD THE NEW WEIGHT
        # data
        weekly_weight = False
        # call method
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight, self.user_created.id)
        # check the returns
        last_weighing_date = ResultsUser.objects.values_list("weighing_date").filter(user=self.user_created).last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        month = calendar.month_name[one_week_after_weighing.month]
        date = "" + calendar.day_name[one_week_after_weighing.weekday()] + " " + str(one_week_after_weighing.day) \
               + " " + month + ""
        self.assertEqual(context["robot_comment"], "Retrouvons nous ici {} pour faire le point sur "
                                                   "tes prochains résultats et voir ton nouveau "
                                                   "challenge !".format(date))

    def test_return_weekly_advice(self):
        """
        test the return of the new advice
        """
        # add the advices to user
        list_advice_id = [1, 4, 8]
        self.add_advice_to_user_created(self.user_created.id, list_advice_id)

        # get user
        user = IdentityUser.objects.get(id=self.user_created.id)

        # check the advice returned if new_week == False :
        # first challenge of the program
        self.new_controller.new_week = False
        return_advice_1 = self.new_controller.return_weekly_advice(self.user_created.id)
        new_advices_user_text_1 = user.advices_to_user.values_list("text").order_by("robot_advice_type").first()[0]
        self.assertEqual(new_advices_user_text_1, return_advice_1)

        id_advice_returned = RobotAdvices.objects.values_list("id").get(text=return_advice_1)[0]
        advice_user_list = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        self.assertEqual(len(advice_user_list), len(list_advice_id))
        self.assertEqual(id_advice_returned, advice_user_list[0][0])

        # check the advice returned if new_week == True :
        # second, ... challenges of the program
        self.new_controller.new_week = True
        return_advice_2 = self.new_controller.return_weekly_advice(self.user_created.id)
        new_advices_user_text_2 = user.advices_to_user.values_list("text").order_by("robot_advice_type").first()[0]
        self.assertEqual(new_advices_user_text_2, return_advice_2)

        id_advice_returned = RobotAdvices.objects.values_list("id").get(text=return_advice_2)[0]
        advice_user_list = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        self.assertEqual(len(advice_user_list), len(list_advice_id) - 1)
        self.assertEqual(id_advice_returned, advice_user_list[0][0])

    def test_save_advices_to_user_first_answer(self):
        """
        test that the method
        add a new advice to user :
        if the user has not answered
        this question yet
        """
        # get the user's advices before of called the method
        user = IdentityUser.objects.get(id=self.user_created.id)
        advice_user_list_before = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advices_before = len(advice_user_list_before)

        # call method
        user_answer_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_advices__isnull=False).first()[0]
        old_question_id = DiscussionSpace.objects.values_list("robot_question").filter(robot_advices__isnull=False).first()[0]
        self.new_controller.save_advices_to_user(user_answer_id, old_question_id, self.user_created.id)

        # get the user's advices after of called the method
        advice_user_list_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advices_after = len(advice_user_list_after)

        self.assertNotEqual(advice_user_list_before, advice_user_list_after)
        self.assertNotEqual(number_advices_before, number_advices_after)

    def test_save_advices_to_user_other_answer(self):
        """
        test that the method
        add a new advice to user
        and that an other advice
        is deleted :
        if the user has answered
        this question yet
        """
        # get the user
        user = IdentityUser.objects.get(id=self.user_created.id)

        # test if the user answer to a question :
        # add a new advice to user
        data = DiscussionSpace.objects.values_list("robot_question")
        for id_question in data:
            user_answer_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_question=id_question).filter(robot_advices__isnull=False)
            if len(user_answer_id) >= 2:
                user_answer = user_answer_id[0][0]
                advice_to_add = DiscussionSpace.objects.values_list("robot_advices").filter(user_answer=user_answer_id[1][0]).filter(robot_question=id_question)[0][0]
                old_question_id = id_question
        list_advice_id = [advice_to_add]
        self.add_advice_to_user_created(self.user_created.id, list_advice_id)

        # get the user's advices before called the method
        advice_user = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_user = len(advice_user)
        id_question_1 = DiscussionSpace.objects.values_list("robot_question").get(robot_advices=advice_user[0][0])

        # call method
        # test if the user change this answer to this question
        self.new_controller.save_advices_to_user(user_answer, old_question_id, self.user_created.id)

        # get the user's advices after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_user_after = len(advice_user_after)
        id_question_2 = DiscussionSpace.objects.values_list("robot_question").get(robot_advices=advice_user_after[0][0])

        self.assertEqual(id_question_1, id_question_2)
        self.assertNotEqual(advice_user, advice_user_after)
        self.assertEqual(number_advice_user, number_advice_user_after)

    def test_return_goal_weight_text_if_incorrect_data(self):
        """
        check the context returned
        if the user's data is incorrect
        """
        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "90"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict, self.user_created.id)

        dict_questions = {"height": "Quelle taille fais-tu ? (au format x,xx)",
                          "actual_weight": "Quel est ton poids actuel ?",
                          "cruising_weight": "Quel est ton poids de croisière (poids le plus longtemps "
                                             "maintenu sans effort) ?",
                          "weight_goal": "Quel est ton poids d'objectif ?"}

        self.assertEqual(len(context), 3)
        self.assertEqual(context["dict_questions"], dict_questions)
        self.assertTrue(context["goal_weight_text"], "Nous allons maintenant définir ton objectif.")
        self.assertTrue(context["error_message"], "Ton objectif doit être inférieur à ton poids actuel.")

    def test_return_goal_weight_text_goal_defined(self):
        """
        check the context returned
        if the goal weight is defined
        """
        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "70"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict, self.user_created.id)

        self.assertEqual(len(context), 1)
        self.assertEqual(context["robot_answer"], "Ton premier objectif de poids a déjà été défini à - {} kg."
                         .format(self.actual_goal))

    def test_return_goal_weight_text_save_weight(self):
        """
        check the context returned
        if the goal weight is not defined
        """
        # delete user's weight data
        ProfileUser.objects.get(user=self.user_created).delete()
        ResultsUser.objects.get(user=self.user_created).delete()

        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "70"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict, self.user_created.id)

        self.assertEqual(len(context), 1)
        self.assertEqual(context["robot_answer"][0:19], "Alors c'est parti !")

    def test_return_start_discussion_display_first_question(self):
        """
        test if the user have don't answers
        to all the questionnaire and have
        not writes this weight goal
        """
        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = False
        user_answer = False

        # call method
        context = self.new_controller.return_start_discussion(self.user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        first_id_question = self.new_questions_list.create_questions_id_list()[0]
        first_question = RobotQuestion.objects.values_list("text").get(id=first_id_question)[0]
        self.assertEqual(len(context), 2)
        self.assertEqual(context["question"], first_question)
        self.assertTrue(context["answers"])

    def test_return_start_discussion_display_second_question(self):
        """
        test if the user have don't answers
        to all the questionnaire and have
        not writes this weight goal
        """
        # get user
        user = IdentityUser.objects.get(id=self.user_created.id)

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        index_id = 0
        old_robot_question_id = self.new_questions_list.create_questions_id_list()[index_id]
        old_robot_question = RobotQuestion.objects.values_list("text").get(id=old_robot_question_id)[0]
        user_answer_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_question=old_robot_question_id).order_by("id").first()[0]
        user_answer = UserAnswer.objects.values_list("text").get(id=user_answer_id)[0]

        # get advices list to the user before called the method
        advice_user_before = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_before = len(advice_user_before)

        # call method
        context = self.new_controller.return_start_discussion(self.user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        # get advices list to the user after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_after = len(advice_user_after)

        second_question_id = self.new_questions_list.create_questions_id_list()[index_id + 1]
        second_question = RobotQuestion.objects.values_list("text").get(id=second_question_id)[0]
        self.assertEqual(context["question"], second_question)
        self.assertTrue(context["answers"])
        self.assertEqual(number_advice_before, number_advice_after - 1)

    def test_return_start_discussion_display_weight_question(self):
        """
        test if the id question list
        is empty : display weight questions
        """
        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question_id = self.new_questions_list.create_questions_id_list()[-1]
        old_robot_question = RobotQuestion.objects.values_list("text").get(id=old_robot_question_id)[0]
        user_answer_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_question=old_robot_question_id).order_by("id").first()[0]
        user_answer = UserAnswer.objects.values_list("text").get(id=user_answer_id)[0]

        # call method
        context = self.new_controller.return_start_discussion(self.user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        dict_questions = {"height": "Quelle taille fais-tu ? (au format x,xx)",
                          "actual_weight": "Quel est ton poids actuel ?",
                          "cruising_weight": "Quel est ton poids de croisière (poids le plus longtemps "
                                             "maintenu sans effort) ?",
                          "weight_goal": "Quel est ton poids d'objectif ?"}
        self.assertEqual(context["robot_answer"], None)
        self.assertEqual(context["goal_weight_text"], "Nous allons maintenant définir ton objectif.")
        self.assertEqual(context["dict_questions"], dict_questions)