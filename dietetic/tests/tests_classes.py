#! /usr/bin/env python3
# coding: UTF-8

"""
TestsReturnWeightAdvicesGoal class
TestsReturnQuestionsList class
TestsController class
TestsCalculation class
"""

# imports
from datetime import date, timedelta
import calendar
import locale
from psycopg2.errors import UniqueViolation
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.calculation import Calculation
from dietetic.classes.controller import Controller
from dietetic.models import DiscussionSpace, RobotQuestion, \
    RobotAdvices, UserAnswer
from account.models import ProfileUser, ResultsUser, StatusUser, \
    HistoryUser, AdvicesToUser
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
# pylint: disable=no-member


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

        self.assertEqual(return_goal, 9)

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
                 "aille en dessous de ce poids. Je tiens donc à te préciser qu'il est " \
                 "possible que tu n'arrives pas à le maintenir sur la durée. " \
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

        self.assertEqual(return_goal, 51)

    def test_return_goal_actual_weight_is_too_low(self):
        """
        test goal returned if the user's
        actual weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        user_goal = "impossible"
        self.assertEqual(return_goal, user_goal)

    def test_return_advice_actual_weight_is_too_low(self):
        """
        test advice returned if the user's
        actual weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids. "
        self.assertEqual(advice, text)

    def test_return_goal_weight_actual_weight_is_too_low(self):
        """
        test goal weight returned if the user's
        actual weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "45",
                            "cruising_weight": "45", "weight_goal": "40"}
        goal_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertFalse(goal_weight)

    def test_return_goal_goal_weight_is_too_low(self):
        """
        test goal returned if the user's
        goal weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(return_goal, 12.6)

    def test_return_advice_goal_weight_is_too_low(self):
        """
        test advice returned if the user's
        goal weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                 "aller en dessous de 47.4 kg. " \
                 "C'est donc l'objectif que nous allons fixer ! "
        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_is_too_low(self):
        """
        test goal weight returned if the user's
        goal weight is too low
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "45", "weight_goal": "40"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertEqual(return_goal, 47.4)

    def test_return_goal_goal_weight_ok(self):
        """
        test goal returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(return_goal, 5)

    def test_return_advice_goal_weight_ok(self):
        """
        test advice returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        advice = "Alors c'est parti ! Partons sur un objectif de - 5 kg. "
        self.assertEqual(return_advice, advice)

    def test_return_goal_weight_goal_weight_ok(self):
        """
        test goal weight returned if the user's
        goal weight is validate
        """
        data_weight_user = {"height": "1,60", "actual_weight": "60",
                            "cruising_weight": "55", "weight_goal": "55"}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertEqual(return_goal, 55)


class TestsReturnQuestionsList(TestCase):
    """ TestsReturnQuestionsList class """

    fixtures = ['data.json']

    def setUp(self):
        self.new_questions_list = QuestionsList()

    def test_return_questions_list(self):
        """
        test the return of the method :
        list that contains the id questions
        """
        return_list = self.new_questions_list.create_questions_id_list()

        id_question_by_type_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 13]
        self.assertEqual(list, type(return_list))
        self.assertEqual(14, len(return_list))
        self.assertEqual(id_question_by_type_list, return_list)


class TestsCalculation(TestCase):
    """ TestsCalculation class """

    fixtures = ['data.json']

    def setUp(self):
        self.user = get_user_model()
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
                advice = RobotAdvices.objects.get(id=id_advice)
                AdvicesToUser.objects.create(user=user_created, advice=advice)
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created

    def test_create_results_data_list(self):
        """
        test the contains
        of the list returned
        """
        user_created = self.create_user()
        list_return = self.new_calculation.create_results_data_list(user_created)

        list_data = [['Semaine', 'Poids'], [0.0, 100.0], [1.0, 95.0]]

        self.assertEqual(list, type(list_return))
        self.assertEqual(str, type(list_return[0][0]))
        self.assertEqual(str, type(list_return[0][1]))
        self.assertEqual(list_data, list_return)
        for elt in list_return:
            self.assertEqual(list, type(elt))
            self.assertEqual(2, len(elt))

    def test_percentage_lost_weight(self):
        """
        test the percentage
        returned by the method
        """
        user_created = self.create_user()
        percentage_return = self.new_calculation.percentage_lost_weight(user_created)

        self.assertEqual(percentage_return, 10)
        self.assertEqual(type(percentage_return), int)

    def test_average_weight_loss(self):
        """
        test average returned
        by the method
        """
        user_created = self.create_user()
        average_return = self.new_calculation.average_weight_loss(user_created)

        self.assertEqual(average_return, 5.0)
        self.assertEqual(type(average_return), float)

    def test_delete_o(self):
        """
        test number returned
        by the method
        """
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
        self.user = get_user_model()
        self.new_controller = Controller()
        self.new_questions_list = QuestionsList()

    def create_new_user(self):
        """
        create a new user
        who has not started
        the program
        """
        username = 'pseudo'
        email = 'carole@tests.com'
        password = '00000000'
        user_created = self.user.objects.create_user(id=1, username=username,
                                                     email=email, password=password)
        HistoryUser.objects.create(user=user_created)
        StatusUser.objects.create(user=user_created)

        return user_created

    def create_user_questionnaire_in_progress(self):
        """
        create a new user
        who is responding
        to the questionnaire
        """
        username = 'pseudo'
        email = 'martine@tests.com'
        password = '00000000'
        user_created = self.user.objects.create_user(id=2, username=username,
                                                     email=email, password=password)
        HistoryUser.objects.create(user=user_created)
        StatusUser.objects.create(user=user_created)
        list_advice_id = [1, 5, 10]
        self.add_advice_to_user_created(user_created, list_advice_id)

        return user_created

    def create_user_start_program_number_days_ago(self, number_days):
        """
        create a user who
        started the program
        """
        username = 'pseudo'
        email = 'nicolas@tests.com'
        password = '00000000'
        user_created = self.user.objects.create_user(id=3, username=username,
                                                     email=email, password=password)
        HistoryUser.objects.create(user=user_created)
        StatusUser.objects.create(user=user_created)
        list_advice_id = [1, 5, 10, 15, 17, 21, 24]
        self.add_advice_to_user_created(user_created, list_advice_id)
        weight = 60
        ProfileUser.objects.create(user=user_created, starting_weight=weight,
                                   actual_goal_weight=10, final_weight=50)
        self.add_user_results(number_days, user_created, weight)
        user = HistoryUser.objects.get(user=user_created)
        user.start_questionnaire_completed = True
        user.save()

        return user_created

    @classmethod
    def add_user_results(cls, number_days, user_created, weight):
        """ add user's results """
        if number_days < 7:
            ResultsUser.objects.create(user=user_created, weight=weight)
        else:
            number_week = number_days / 7
            number_week_list = list(range(1, int(number_week) + 1))
            last_weight = weight - int(number_week)
            for elt in number_week_list:
                days = elt * 7
                weighing_date = date.today() - timedelta(days=int(days))
                ResultsUser.objects.create(user=user_created,
                                           weighing_date=weighing_date,
                                           weight=last_weight + elt)

    def create_user_start_program_advices_list_empty(self):
        """
        create a user who
        started the program
        but does not have
        advices
        """
        username = 'pseudo'
        email = 'christiane@tests.com'
        password = '00000000'
        user_created = self.user.objects.create_user(id=4, username=username,
                                                     email=email, password=password)
        HistoryUser.objects.create(user=user_created)
        StatusUser.objects.create(user=user_created)
        weight = 60
        ProfileUser.objects.create(user=user_created, starting_weight=weight,
                                   actual_goal_weight=10, final_weight=50)
        self.add_user_results(50, user_created, weight)
        user = HistoryUser.objects.get(user=user_created)
        user.start_questionnaire_completed = True
        user.save()

        return user_created

    @classmethod
    def add_advice_to_user_created(cls, user, list_advice_id):
        """
        add new advices
        to the user
        """
        for id_advice in list_advice_id:
            advice = RobotAdvices.objects.get(id=id_advice)
            AdvicesToUser.objects.create(user=user, advice=advice)

    def test_parser_weight(self):
        """ test parser_weight method """
        # if the data is correct
        data_weight_user = {"height": "1,60", "actual_weight": "100",
                            "cruising_weight": "50", "weight_goal": "50"}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        self.assertTrue(return_validate)
        self.assertEqual(return_context, {})

        # if the data is not correct
        data_weight_user = {"height": "1,60", "actual_weight": "50",
                            "cruising_weight": "50", "weight_goal": "60"}
        return_validate = self.new_controller.parser_weight(data_weight_user)[0]
        return_context = self.new_controller.parser_weight(data_weight_user)[1]
        text = "Ton objectif doit être inférieur à ton poids actuel."
        self.assertFalse(return_validate)
        self.assertEqual(return_context, {"error_message": text})
        self.assertEqual(type(return_context), dict)

    def test_return_text_congratulations_restart_program(self):
        """ test return_text_congratulations_restart_program method """
        # create user
        user_created = self.create_user_start_program_number_days_ago(60)
        # get data
        pseudo = user_created.username

        # user's data before
        # called method
        advice_user_before = AdvicesToUser.objects.filter(user=user_created)
        data_profile_before = ProfileUser.objects.get(user=user_created)
        data_results_before = ResultsUser.objects.filter(user=user_created)
        before_method = HistoryUser.objects.values_list("start_questionnaire_completed")\
            .get(user=user_created)[0]

        # call method
        return_text = self.new_controller.return_text_congratulations_restart_program\
            (user_created.id)

        # user's data after
        # called method
        advice_user_after = AdvicesToUser.objects.filter(user=user_created)
        data_profile_after = ProfileUser.objects.filter(user=user_created)
        data_results_after = ResultsUser.objects.filter(user=user_created)
        after_method = HistoryUser.objects.values_list("start_questionnaire_completed")\
            .get(user=user_created)[0]

        text = "Félicitation {} ! Tu as atteints ton objectif !".format(pseudo)
        self.assertFalse(after_method)
        self.assertNotEqual(before_method, after_method)
        self.assertEqual(type(return_text), str)
        self.assertEqual(return_text, text)
        self.assertEqual(len(data_profile_after), 0)
        self.assertEqual(len(data_results_after), 0)
        self.assertEqual(len(advice_user_after), 0)
        self.assertNotEqual(data_profile_before, data_profile_after)
        self.assertNotEqual(data_results_before, data_results_after)
        self.assertNotEqual(advice_user_before, advice_user_after)

    def test_add_advices_to_user(self):
        """
        test that the method add
        a new challenges to user
        """
        # create user
        user_created = self.create_user_start_program_advices_list_empty()

        # count the number of challenges
        # before a call to the method
        user = self.user.objects.get(id=user_created.id)
        number_advice_to_user_before = user.advices_to_user.count()

        # call method
        self.new_controller.add_advices_to_user(user_created.id)

        # count the number of challenges
        # after a call to the method
        number_advice_to_user_after = user.advices_to_user.count()
        advice_to_user = user.advices_to_user.values_list("id")
        self.assertEqual(number_advice_to_user_before, 0)
        self.assertEqual(number_advice_to_user_after, 5)
        for id_advice in advice_to_user:
            self.assertEqual([(27,), (28,), (29,), (25,), (26,)].count(id_advice), 1)

    def test_return_weekly_questions_save_weight(self):
        """
        test the returns of the method
        and check that the weight is save
        """
        # create user
        user_created = self.create_user_start_program_number_days_ago(7)

        # TEST NEW WEIGHT DON'T EXISTS
        # data
        weekly_weight = False

        # call method
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight,
                                                                          user_created.id)

        self.assertEqual(context["robot_comment"], "Bonjour ! J'éspère que ta semaine "
                                                   "s'est bien passée ? "
                                                   "Que donne ta pesée ce matin ?")
        self.assertTrue(context["robot_weekly_weight"])

        # TEST ADD THE NEW WEIGHT
        # data
        weekly_weight = 58

        # call method
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight,
                                                                          user_created.id)

        last_weight = ResultsUser.objects.values_list("weight").filter(user=user_created)\
            .order_by("weighing_date").last()[0]
        self.assertEqual(context["robot_comment"], "J'ai bien pris note de ton poids, "
                                                   "tu trouveras un récapitulatif dans "
                                                   "l'onglet résultats.")
        self.assertEqual(last_weight, weekly_weight)

        # TEST AFTER ADD THE NEW WEIGHT
        # data
        weekly_weight = False

        # call method
        context = self.new_controller.return_weekly_questions_save_weight(weekly_weight,
                                                                          user_created.id)

        last_weighing_date = ResultsUser.objects.values_list("weighing_date")\
            .filter(user=user_created).order_by("weighing_date").last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        month = calendar.month_name[one_week_after_weighing.month]
        date_next_challenge = "" + calendar.day_name[one_week_after_weighing.weekday()] + " " \
                              + str(one_week_after_weighing.day) + " " + month + ""
        self.assertEqual(context["robot_comment"], "Retrouvons nous ici {} pour faire le point sur "
                                                   "tes prochains résultats et voir ton nouveau "
                                                   "challenge !".format(date_next_challenge))

    def test_return_weekly_advice(self):
        """
        test the return
        of the new advice
        """
        # create and get user
        user_created = self.create_user_start_program_number_days_ago(7)
        user = self.user.objects.get(id=user_created.id)

        # check the advice returned if new_week == False :
        # first challenge of the program
        self.new_controller.new_week = False
        return_advice_1 = self.new_controller.return_weekly_advice(user_created.id)
        new_advices_user_text_1 = "J'analyse : La deuxième semaine est une semaine particulière"
        self.assertEqual(new_advices_user_text_1, return_advice_1[:60])

        id_advice_returned = RobotAdvices.objects.values_list("id").get(text=return_advice_1)[0]
        advice_user_list = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        self.assertEqual(id_advice_returned, advice_user_list[0][0])

        # check the advice returned if new_week == True :
        # second, ... challenges of the program
        self.new_controller.new_week = True
        return_advice_2 = self.new_controller.return_weekly_advice(user_created.id)
        new_advices_user_text_2 = "Une faim de loup ! : Tu m'as indiqué dans ton questionnaire"
        self.assertEqual(new_advices_user_text_2, return_advice_2[:59])

        id_advice_returned = RobotAdvices.objects.values_list("id").get(text=return_advice_2)[0]
        advice_user_list = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        self.assertEqual(id_advice_returned, advice_user_list[0][0])

    def test_save_advices_to_user_first_answer(self):
        """
        test that the method
        add a new advice to user :
        if the user has not answered
        this question yet
        """
        # create user
        user_created = self.create_new_user()

        # get the user's advices
        # before of called the method
        user = self.user.objects.get(id=user_created.id)
        advice_user_list_before = user.advices_to_user.values_list("id")\
            .order_by("robot_advice_type")
        number_advices_before = len(advice_user_list_before)

        # call method
        user_answer_id = DiscussionSpace.objects.values_list("user_answer")\
            .filter(robot_advices__isnull=False).first()[0]
        old_question_id = DiscussionSpace.objects.values_list("robot_question")\
            .filter(robot_advices__isnull=False).first()[0]
        self.new_controller.save_advices_to_user(user_answer_id, old_question_id, user_created.id)

        # get the user's advices
        # after of called the method
        advice_user_list_after = user.advices_to_user.values_list("id")\
            .order_by("robot_advice_type")
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
        # create and get user
        user_created = self.create_new_user()
        user = self.user.objects.get(id=user_created.id)

        # test if the user answer to a question :
        # add a new advice to user
        data = DiscussionSpace.objects.values_list("robot_question")
        for id_question in data:
            user_answer_id = DiscussionSpace.objects.values_list("user_answer")\
                .filter(robot_question=id_question).filter(robot_advices__isnull=False)
            if len(user_answer_id) >= 2:
                user_answer = user_answer_id[0][0]
                advice_to_add = DiscussionSpace.objects.values_list("robot_advices")\
                    .filter(user_answer=user_answer_id[1][0])\
                    .filter(robot_question=id_question)[0][0]
                old_question_id = id_question
        list_advice_id = [advice_to_add]
        self.add_advice_to_user_created(user_created, list_advice_id)

        # get the user's advices
        # before called the method
        advice_user = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_user = len(advice_user)
        id_question_1 = DiscussionSpace.objects.values_list("robot_question")\
            .get(robot_advices=advice_user[0][0])

        # call method
        # test if the user change
        # this answer to this question
        self.new_controller.save_advices_to_user(user_answer, old_question_id,
                                                 user_created.id)

        # get the user's advices
        # after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_user_after = len(advice_user_after)
        id_question_2 = DiscussionSpace.objects.values_list("robot_question")\
            .get(robot_advices=advice_user_after[0][0])

        self.assertEqual(id_question_1, id_question_2)
        self.assertNotEqual(advice_user, advice_user_after)
        self.assertEqual(number_advice_user, number_advice_user_after)

    def test_return_goal_weight_text_if_incorrect_data(self):
        """
        check the context returned
        if the user's data is incorrect
        """
        # create user
        user_created = self.create_user_questionnaire_in_progress()

        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "90"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict,
                                                                          user_created.id)

        dict_questions = {"height": "Quelle taille fais-tu ? (au format x,xx)",
                          "actual_weight": "Quel est ton poids actuel ?",
                          "cruising_weight": "Quel est ton poids de croisière "
                                             "(poids le plus longtemps "
                                             "maintenu sans effort) ?",
                          "weight_goal": "Quel est ton poids d'objectif ?"}

        self.assertEqual(len(context), 3)
        self.assertEqual(context["dict_questions"], dict_questions)
        self.assertTrue(context["goal_weight_text"], "Nous allons maintenant définir ton objectif.")
        self.assertTrue(context["error_message"], "Ton objectif doit être inférieur "
                                                  "à ton poids actuel.")

    def test_return_goal_weight_text_goal_defined(self):
        """
        check the context returned
        if the goal weight is defined
        """
        # create user
        user_created = self.create_user_start_program_number_days_ago(0)

        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "70"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict,
                                                                          user_created.id)

        self.assertEqual(len(context), 1)
        self.assertEqual(context["robot_answer"][:40], "Ton premier objectif de poids a déjà été")

    def test_return_goal_weight_text_save_weight(self):
        """
        check the context returned
        if the goal weight is not defined
        """
        # create user
        user_created = self.create_user_questionnaire_in_progress()

        # data
        data_dict = {"height": "1,60", "actual_weight": "80",
                     "cruising_weight": "50", "weight_goal": "70"}

        # call method
        context = self.new_controller.return_goal_weight_text_save_weight(data_dict,
                                                                          user_created.id)

        self.assertEqual(len(context), 1)
        self.assertEqual(context["robot_answer"][0:19], "Alors c'est parti !")

    def test_return_start_discussion_display_first_question(self):
        """
        test if the user have don't answers
        to all the questionnaire and have
        not writes this weight goal
        """
        # create user
        user_created = self.create_new_user()

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = False
        user_answer = False

        # call method
        context = self.new_controller.return_start_discussion(user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        first_question = "Bonjour, je me présente \"My Dietetic Challenge\" !"
        self.assertEqual(len(context), 2)
        self.assertEqual(context["question"][:49], first_question)
        self.assertTrue(context["answers"])
        self.assertEqual(type(context["answers"]), list)
        self.assertEqual(len(context["answers"]), 3)

    def test_return_start_discussion_display_second_question(self):
        """
        test if the user have don't answers
        to all the questionnaire and have
        not writes this weight goal
        """
        # create and get user
        user_created = self.create_new_user()
        user = self.user.objects.get(id=user_created.id)

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = "Bonjour, je me présente \"My Dietetic Challenge\" ! " \
                             "Mon objectif à partir d'aujourd'hui est de t'aider dans " \
                             "ton parcours de perte de poids en la rendant plus attrayante ! " \
                             "Mais avant de nous lancer dans cette FOLLE aventure, " \
                             "j'ai besoin d'en connaître plus sur toi ! Es-tu prêt(e) ?"
        user_answer = "oui"

        # get advices list to the user before called the method
        advice_user_before = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_before = len(advice_user_before)

        # call method
        context = self.new_controller.return_start_discussion(user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        # get advices list to the user after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice_after = len(advice_user_after)

        second_question = "D'après toi, as-tu des connaissances en diététique " \
                          "suffisantes pour t'aider à perdre du poids ?"
        robot_answer = "Alors c'est parti ! Voici mes questions …"
        self.assertTrue(context["question"])
        self.assertEqual(context["question"][:95], second_question)
        self.assertTrue(context["answers"])
        self.assertEqual(type(context["answers"]), list)
        self.assertEqual(len(context["answers"]), 3)
        self.assertTrue(context["robot_answer"])
        self.assertEqual(context["robot_answer"][:41], robot_answer)
        self.assertEqual(number_advice_before, number_advice_after - 1)

    def test_return_start_discussion_display_weight_question(self):
        """
        test if the id question list
        is empty : display weight questions
        """
        # create user
        user_created = self.create_user_questionnaire_in_progress()

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = "Grignotes-tu après les repas ?"
        user_answer = "non"

        # call method
        context = self.new_controller.return_start_discussion(user_created.id, old_robot_question,
                                                              data_dict, user_answer)

        dict_questions = {"height": "Quelle taille fais-tu ? (au format x,xx)",
                          "actual_weight": "Quel est ton poids actuel ?",
                          "cruising_weight": "Quel est ton poids de croisière "
                                             "(poids le plus longtemps "
                                             "maintenu sans effort) ?",
                          "weight_goal": "Quel est ton poids d'objectif ?"}
        self.assertEqual(context["robot_answer"], None)
        self.assertEqual(context["goal_weight_text"], "Nous allons maintenant "
                                                      "définir ton objectif.")
        self.assertEqual(len(context["dict_questions"]), 4)
        self.assertEqual(context["dict_questions"], dict_questions)

    def test_return_start_discussion_display_end_discussion_answer_2(self):
        """
        test if the user selects the answer
        2 to the first question :
        end discussion
        """
        # create and get user
        user_created = self.create_new_user()
        user = self.user.objects.get(id=user_created.id)

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = "Bonjour, je me présente \"My Dietetic Challenge\" ! " \
                             "Mon objectif à partir d'aujourd'hui est de t'aider dans " \
                             "ton parcours de perte de poids en la rendant plus attrayante ! " \
                             "Mais avant de nous lancer dans cette FOLLE aventure, " \
                             "j'ai besoin d'en connaître plus sur toi ! Es-tu prêt(e) ?"
        user_answer = "non"

        # call method
        context = self.new_controller.return_start_discussion(user_created.id,
                                                              old_robot_question,
                                                              data_dict,
                                                              user_answer)

        # get advices list to the user
        # after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice = len(advice_user_after)

        self.assertEqual(context["robot_answer"], 'Dommage… une autre fois peut-être !')
        self.assertEqual(number_advice, 0)

    def test_return_start_discussion_display_end_discussion_answer_3(self):
        """
        test if the user selects the answer
        3 to the first question :
        end discussion
        """
        # create and get user
        user_created = self.create_new_user()
        user = self.user.objects.get(id=user_created.id)

        # data
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        old_robot_question = "Bonjour, je me présente \"My Dietetic Challenge\" ! " \
                             "Mon objectif à partir d'aujourd'hui est de t'aider dans " \
                             "ton parcours de perte de poids en la rendant plus attrayante ! " \
                             "Mais avant de nous lancer dans cette FOLLE aventure, " \
                             "j'ai besoin d'en connaître plus sur toi ! Es-tu prêt(e) ?"
        user_answer = "j'hésite encore ..."

        # call method
        context = self.new_controller.return_start_discussion(user_created.id,
                                                              old_robot_question,
                                                              data_dict,
                                                              user_answer)

        # get advices list to the user
        # after called the method
        advice_user_after = user.advices_to_user.values_list("id").order_by("robot_advice_type")
        number_advice = len(advice_user_after)

        self.assertEqual(context["robot_answer"], 'Très bien ! Je reste à ta '
                                                  'disposition et me tiens prêt '
                                                  'lorsque ta motivation sera au '
                                                  'plus haut.')
        self.assertEqual(number_advice, 0)

    def test_controller_dietetic_space_view_start_questionnaire_completed_false(self):
        """
        tests context returned
        if the user have not answered
        to the robot questions
        """
        # create user
        user_created = self.create_new_user()

        # data
        old_robot_question = "Bonjour, je me présente \"My Dietetic Challenge\" ! " \
                             "Mon objectif à partir d'aujourd'hui est de t'aider dans " \
                             "ton parcours de perte de poids en la rendant plus attrayante ! " \
                             "Mais avant de nous lancer dans cette FOLLE aventure, " \
                             "j'ai besoin d'en connaître plus sur toi ! Es-tu prêt(e) ?"
        user_answer = "oui"
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        weekly_weight = False

        advice_user = AdvicesToUser.objects.filter(user=user_created)
        number_advices_before = len(advice_user)

        # call method
        context = self.new_controller.controller_dietetic_space_view(user_created.id,
                                                                     old_robot_question,
                                                                     data_dict, user_answer,
                                                                     weekly_weight)

        advice_user = AdvicesToUser.objects.filter(user=user_created)
        number_advices_after = len(advice_user)
        robot_question = "D'après toi, as-tu des connaissances en diététique " \
                         "suffisantes pour t'aider à perdre du poids ?"
        robot_answer = "Alors c'est parti ! Voici mes questions …"
        self.assertEqual(len(context), 3)
        self.assertTrue(context["robot_answer"])
        self.assertEqual(context["robot_answer"], robot_answer)
        self.assertTrue(context["question"])
        self.assertEqual(context["question"], robot_question)
        self.assertTrue(context["answers"])
        self.assertEqual(type(context["answers"]), list)
        self.assertEqual(len(context["answers"]), 3)
        self.assertEqual(number_advices_before, 0)
        self.assertEqual(number_advices_after, 1)

    def test_controller_dietetic_space_view_start_questionnaire_completed_true_ww_false(self):
        """
        tests context returned
        if the user has started
        the program
        """
        # create user
        user_created = self.create_user_start_program_number_days_ago(7)

        # data
        old_robot_question = False
        user_answer = False
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        weekly_weight = False

        # call method
        context = self.new_controller.controller_dietetic_space_view(user_created.id,
                                                                     old_robot_question,
                                                                     data_dict, user_answer,
                                                                     weekly_weight)

        robot_comment = "Bonjour ! J'éspère que ta semaine s'est bien passée ? " \
                        "Que donne ta pesée ce matin ?"
        advice = "J'analyse : La deuxième semaine est une semaine particulière …"
        self.assertTrue(context["robot_comment"])
        self.assertEqual(context["robot_comment"], robot_comment)
        self.assertTrue(context["robot_weekly_weight"])
        self.assertTrue(context["advice"])
        self.assertEqual(context["advice"][:62], advice)

    def test_controller_dietetic_space_view_start_questionnaire_completed_true_ww_true(self):
        """
        tests context returned
        if the user has started
        the program and has wrote
        this weekly weight
        """
        # create user
        user_created = self.create_user_start_program_number_days_ago(7)

        # data
        old_robot_question = False
        user_answer = False
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        weekly_weight = 58

        advice_user = AdvicesToUser.objects.filter(user=user_created)
        number_advices_before = len(advice_user)

        # call method
        context = self.new_controller.controller_dietetic_space_view(user_created.id,
                                                                     old_robot_question,
                                                                     data_dict, user_answer,
                                                                     weekly_weight)

        advice_user = AdvicesToUser.objects.filter(user=user_created)
        number_advices_after = len(advice_user)
        results_user = ResultsUser.objects.values_list("weight").filter(user=user_created)\
            .order_by("weighing_date")
        robot_comment = "J'ai bien pris note de ton poids, tu trouveras " \
                        "un récapitulatif dans l'onglet résultats."
        advice = "Une faim de loup ! : Tu m'as indiqué"
        self.assertTrue(context["robot_comment"])
        self.assertEqual(context["robot_comment"], robot_comment)
        self.assertTrue(context["advice"])
        self.assertEqual(context["advice"][:36], advice)
        self.assertEqual(len(results_user), 2)
        self.assertEqual(results_user[1][0], 58)
        self.assertEqual(number_advices_after + 1, number_advices_before)

    def test_controller_dietetic_space_view_start_questionnaire_completed_true_ww_goal(self):
        """
        tests context returned
        if the user has started
        the program and has wrote
        this weekly weight
        """
        # create user
        user_created = self.create_user_start_program_number_days_ago(60)

        # data
        old_robot_question = False
        user_answer = False
        data_dict = {"height": False, "actual_weight": False,
                     "cruising_weight": False, "weight_goal": False}
        weekly_weight = 50

        # call method
        context = self.new_controller.controller_dietetic_space_view(user_created.id,
                                                                     old_robot_question,
                                                                     data_dict, user_answer,
                                                                     weekly_weight)

        advice_user = AdvicesToUser.objects.filter(user=user_created)
        results_user = ResultsUser.objects.filter(user=user_created)
        profile_user = ProfileUser.objects.filter(user=user_created)
        user = HistoryUser.objects.get(user=user_created.id)
        robot_comment = 'Félicitation pseudo ! Tu as atteints ton objectif !'
        self.assertTrue(context["robot_comment"])
        self.assertEqual(len(context), 1)
        self.assertEqual(context["robot_comment"], robot_comment)
        self.assertEqual(len(results_user), 0)
        self.assertEqual(len(profile_user), 0)
        self.assertFalse(user.start_questionnaire_completed)
        self.assertEqual(len(advice_user), 0)
