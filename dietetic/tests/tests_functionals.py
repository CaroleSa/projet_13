#! /usr/bin/env python3
# coding: UTF-8

""" TestsFunctionals class - dietetic app """

# imports
import random
from datetime import date, timedelta
import calendar
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
'fr_FR'
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser, StatusUser
from dietetic.models import DiscussionSpace, RobotQuestionType, RobotQuestion, UserAnswer
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.calculation import Calculation
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.db import connection
from selenium import webdriver, common
from psycopg2.errors import UniqueViolation



class TestsFunctionals(StaticLiveServerTestCase):
    """ class TestsFunctionals :
    test the use of the dietetic challenge """

    fixtures = ['data.json']

    def setUp(self):
        self.user = get_user_model()
        self.browser = webdriver.Firefox()
        self.cursor = connection.cursor()
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.new_calculation = Calculation()
        self.question = ""

    def tearDown(self):
        self.browser.quit()

    def create_user_not_start_program(self):
        """ create a new user """
        dict_data_user = {"id_email": "carole1@test.fr", "id_password": "00000000"}
        id_user = 1
        try:
            user_created = self.user.objects.create_user(id=id_user, username="pseudo",
                                                         email=dict_data_user.get('id_email'),
                                                         password=dict_data_user.get('id_password'))
            HistoryUser.objects.create(user=user_created)
            StatusUser.objects.create(user=user_created)
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created, dict_data_user

    def create_user_starting_program(self):
        """
        create a user
        who started program
        """
        dict_data_user = {"id_email": "carole2@test.fr", "id_password": "00000000"}
        id_user = 2
        try:
            user_created = self.user.objects.create_user(id=id_user, username="pseudo",
                                                         email=dict_data_user.get('id_email'),
                                                         password=dict_data_user.get('id_password'))
            HistoryUser.objects.create(user=user_created)
            StatusUser.objects.create(user=user_created)
            ProfileUser.objects.create(user=user_created, starting_weight=100,
                                       actual_goal_weight=50, final_weight=50)
            ResultsUser.objects.create(user=user_created, weight=100)
            user = HistoryUser.objects.get(user=user_created)
            user.start_questionnaire_completed = True
            user.save()
            self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                                "VALUES ({}, {})".format(id_user, 1))
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created, dict_data_user

    def create_user_one_week_ago(self):
        """
            create a user
            who has been following
            the program for one week
        """
        dict_data_user = {"id_email": "carole3@test.fr", "id_password": "00000000"}
        id_user = 3
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
            user = HistoryUser.objects.get(user=user_created)
            user.start_questionnaire_completed = True
            user.save()
            list_advice_id = [1, 4]
            for id_advice in list_advice_id:
                self.cursor.execute("INSERT INTO account_identityuser_advices_to_user "
                                    "(identityuser_id, robotadvices_id) "
                                    "VALUES ({}, {})".format(id_user, id_advice))
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created, dict_data_user

    def create_user_without_challenge(self):
        """
            create a user
            who has been following
            the program but have
            not challenges
            in the challenge list
        """
        dict_data_user = {"id_email": "carole4@test.fr", "id_password": "00000000"}
        id_user = 4
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
            user = HistoryUser.objects.get(user=user_created)
            user.start_questionnaire_completed = True
            user.save()
            self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                                "VALUES ({}, {})".format(id_user, 1))
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created, dict_data_user

    def create_user_two_weeks_ago(self):
        """
        create a user
        who has been following
        the program for two weeks
        """
        dict_data_user = {"id_email": "carole5@test.fr", "id_password": "00000000"}
        id_user = 5
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
            list_advice_id = [1, 4]
            for id_advice in list_advice_id:
                self.cursor.execute("INSERT INTO account_identityuser_advices_to_user "
                                    "(identityuser_id, robotadvices_id) "
                                    "VALUES ({}, {})".format(id_user, id_advice))
        except (UniqueViolation, IntegrityError):
            user_created = self.user.objects.get(id=id_user)

        return user_created, dict_data_user

    def login_user(self, dict_login):
        """ login user """
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        for key, value in dict_login.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

    def test_access_home_page(self):
        """
        test if the user clicks
        to the home nav
        """
        # get user's data
        user_data = self.create_user_not_start_program()[1]

        # login user
        self.login_user(user_data)

        # test access home page
        self.browser.find_element_by_id("home").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/")

    def test_questionnaire_answer_two_or_three(self):
        """
        test if the user choices
        the second and third answer
        to the first robot question
        """
        # get user's data
        user_data = self.create_user_not_start_program()[1]

        # login user
        self.login_user(user_data)

        # check robot answer if the user choices the answers 2 or 3
        dict_user_robot_answer = {2: "Dommage… une autre fois peut-être !",
                                  3: "Très bien ! Je reste à ta disposition et me tiens prêt "
                                     "lorsque ta motivation sera au plus haut."}
        for user_answer_id, robot_answer_text in dict_user_robot_answer.items():
            # access dietetic space page
            self.browser.find_element_by_id("clipboard").click()
            # test user's answer
            answer_text = UserAnswer.objects.values_list("text").get(id=user_answer_id)[0]
            self.browser.find_element_by_id(answer_text).click()
            self.browser.find_element_by_id("validate_button").click()
            robot_answer = self.browser.find_element_by_id("robot_answer").text
            self.assertEqual(robot_answer, robot_answer_text)

    def test_questionnaire(self):
        """
        test if the user choices
        the first answer
        to the first robot question
        """
        # get user's data
        user_data = self.create_user_not_start_program()[1]
        user_created = self.create_user_not_start_program()[0]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/dietetic/dietetic_space/")

        # test if the user clicks on the first answer
        answer_text = UserAnswer.objects.values_list("text").get(id=1)[0]
        self.browser.find_element_by_id(answer_text).click()
        self.browser.find_element_by_id("validate_button").click()

        # after, the user choices the random answer
        while 1:
            try:
                self.question = self.browser.find_element_by_id("robot_question").text
                id_robot_question = RobotQuestion.objects.values_list("id").get(text=self.question)
                number_answers = DiscussionSpace.objects.values_list("user_answer").filter(
                    robot_question=id_robot_question).order_by("id").count()
                number = random.randint(0, number_answers - 1)
                user_answer_id = \
                DiscussionSpace.objects.values_list("user_answer").filter(robot_question=id_robot_question)[number][0]
                user_answer_text = UserAnswer.objects.values_list("text").get(id=user_answer_id)[0]
                self.browser.find_element_by_id(user_answer_text).click()
                self.browser.find_element_by_id("validate_button").click()
            except common.exceptions.NoSuchElementException:
                break

        # check the next questions value
        id_elt_question_text_dict = {"goal_weight_text": "Nous allons maintenant définir ton objectif.",
                                     "question_height": "Quelle taille fais-tu ? (au format x,xx)",
                                     "question_actual_weight": "Quel est ton poids actuel ?",
                                     "question_cruising_weight": "Quel est ton poids de croisière "
                                                                 "(poids le plus longtemps maintenu sans effort) ?",
                                     "question_weight_goal": "Quel est ton poids d'objectif ?"}
        for id_elt, question_text in id_elt_question_text_dict.items():
            question = self.browser.find_element_by_id(id_elt).text
            self.assertEqual(question, question_text)

        # user writes this goal weight, ...
        dict_data = {"height": "1,60", "actual_weight": "60", "cruising_weight": "50", "weight_goal": "50"}
        for key, value in dict_data.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("validate_goal").click()

        # check the robot answer
        advice = self.new_weight_advice_goal.return_weight_advices_goal(dict_data)[1]
        id_type = RobotQuestionType.objects.values_list("id").get(type="end start")[0]
        start_text_end = RobotQuestion.objects.values_list("text").get(robot_question_type=id_type)[0]
        text = advice + start_text_end
        robot_answer = self.browser.find_element_by_id("robot_answer").text
        self.assertEqual(text, robot_answer)

        last_weighing_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        month = calendar.month_name[one_week_after_weighing.month]
        date = "" + calendar.day_name[one_week_after_weighing.weekday()] + " " + str(one_week_after_weighing.day) \
               + " " + month + ""
        robot_text = "Retrouvons nous ici {} pour faire le point sur tes prochains résultats " \
                     "et voir ton nouveau challenge !".format(date)
        text = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(text, robot_text)

        # check that card is display
        try:
            self.browser.find_element_by_id("card").click()
            challenge = self.browser.find_element_by_id("dietetic_text").text
            self.assertNotEqual(challenge, "")
            display_card = True
        except common.exceptions.NoSuchElementException:
            display_card = False
        self.assertTrue(display_card)

    def test_access_discussion_space_first_week(self):
        """
        test if the user clicks
        to the discussion space
        during the first week
        """
        # get user's data
        user_data = self.create_user_starting_program()[1]
        user_created = self.create_user_starting_program()[0]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()

        # check the element display
        try:
            self.browser.find_element_by_id("robot_answer")
            answer = True
        except common.exceptions.NoSuchElementException:
            answer = False
        self.assertFalse(answer)

        last_weighing_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        month = calendar.month_name[one_week_after_weighing.month]
        date = "" + calendar.day_name[one_week_after_weighing.weekday()] + " " + str(one_week_after_weighing.day) \
               + " " + month + ""
        robot_text = "Retrouvons nous ici {} pour faire le point sur tes prochains résultats " \
                     "et voir ton nouveau challenge !".format(date)
        text = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(text, robot_text)

        # check that card is display
        try:
            self.browser.find_element_by_id("card").click()
            challenge = self.browser.find_element_by_id("dietetic_text").text
            self.assertNotEqual(challenge, "")
            display_card = True
        except common.exceptions.NoSuchElementException:
            display_card = False
        self.assertTrue(display_card)

    def test_access_my_result_page_first_week(self):
        """
        test the access in the result page
        check the elements display
        during the first week
        """
        # get user's data
        user_data = self.create_user_starting_program()[1]
        user_created = self.create_user_starting_program()[0]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("poll").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/dietetic/my_results/")
        
        # check graphic is not display
        try:
            self.browser.find_element_by_id("graphic_my_results")
            graphic = True
        except common.exceptions.NoSuchElementException:
            graphic = False
        self.assertFalse(graphic)
        
        # check values data display
        text_display = self.browser.find_element_by_id("starting_date").text
        starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).first()[0]
        month = calendar.month_name[starting_date.month]
        starting_date = "" + str(starting_date.day) + " " + month + " " + str(starting_date.year) + ""
        text = "Suivi démarré le {}".format(starting_date)
        self.assertEqual(text, text_display)

        text_display = self.browser.find_element_by_id("starting_goal_weight").text
        starting_weight = ProfileUser.objects.values_list("starting_weight").get(user=user_created)[0]
        final_weight = ProfileUser.objects.values_list("final_weight").get(user=user_created)[0]
        text = "Poids de départ : {} kg\nPoids d'objectif : {} kg".format(self.new_calculation.delete_o(starting_weight),
                                                                          self.new_calculation.delete_o(final_weight))
        self.assertEqual(text, text_display)

        text_display = self.browser.find_element_by_id("goal_weight").text
        goal_weight = ProfileUser.objects.values_list("actual_goal_weight").get(user=user_created)[0]
        text = "Ton objectif est de - {} kg".format(self.new_calculation.delete_o(goal_weight))
        self.assertEqual(text, text_display)

        text_display = self.browser.find_element_by_id("no_results").text
        text = "Pas de résultats pour le moment.\nSuis l'évolution de ton " \
               "poids sur un graphique dès la semaine prochaine."
        self.assertEqual(text, text_display)

    def test_access_my_result_page_next_weeks(self):
        """
        test the access in the result page
        check the elements display
        during the next weeks
        """
        # get user's data
        user_data = self.create_user_two_weeks_ago()[1]
        user_created = self.create_user_two_weeks_ago()[0]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("poll").click()

        # check graphic is display
        try:
            self.browser.find_element_by_id("graphic_my_results")
            graphic = True
        except common.exceptions.NoSuchElementException:
            graphic = False
        self.assertTrue(graphic)

        # check values data display
        text_display = self.browser.find_element_by_id("starting_date").text
        starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=user_created).first()[0]
        month = calendar.month_name[starting_date.month]
        date = "" + str(starting_date.day) + " " + month + " " \
               + str(starting_date.year) + ""
        text = "Suivi démarré le {}".format(date)
        self.assertEqual(text, text_display)

        text_display = self.browser.find_element_by_id("starting_goal_weight").text
        starting_weight = ProfileUser.objects.values_list("starting_weight").get(user=user_created)[0]
        final_weight = ProfileUser.objects.values_list("final_weight").get(user=user_created)[0]
        text = "Poids de départ : {} kg\nPoids d'objectif : {} kg".format(self.new_calculation.delete_o(starting_weight),
                                                                          self.new_calculation.delete_o(final_weight))
        self.assertEqual(text, text_display)

        text_display = self.browser.find_element_by_id("goal_weight").text
        goal_weight = ProfileUser.objects.values_list("actual_goal_weight").get(user=user_created)[0]
        text = "Ton objectif est de - {} kg".format(self.new_calculation.delete_o(goal_weight))
        self.assertEqual(text, text_display)

        percentage = self.new_calculation.percentage_lost_weight(user_created)
        average = self.new_calculation.average_weight_loss(user_created)
        last_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).last()[0]
        starting_weight = ResultsUser.objects.values_list("weight").filter(user=user_created).first()[0]
        total_goal = float(starting_weight - last_weight)
        text_display = self.browser.find_element_by_id("results_display").text
        text = "Tu as perdu {} kg :\ncela correspond à {} % de ton objectif." \
               "\nTa perte moyenne est de {} kg par semaine.".\
            format(self.new_calculation.delete_o(total_goal),
                   percentage, self.new_calculation.delete_o(average))
        self.assertEqual(text, text_display)

    def test_access_program_page(self):
        """
        test the access in the program page
        check the elements display
        """
        # get user's data
        user_data = self.create_user_starting_program()[1]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("program").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/dietetic/program/")

        # check graphic is not display
        titre = self.browser.find_element_by_id("title-meal").text
        self.assertEqual(titre, "Petit-déjeuner :")

    def test_access_discussion_space_week_end(self):
        """
        test if the user clicks
        to the discussion space
        during the week-end
        """
        # get user's data
        user_data = self.create_user_one_week_ago()[1]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()

        # old challenge
        self.browser.find_element_by_id("card").click()
        old_challenge = self.browser.find_element_by_id("dietetic_text").text

        # check the element display
        question = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(question, "Bonjour ! J'éspère que ta semaine s'est bien passée ? Que donne ta pesée ce matin ?")

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("85")
        self.browser.find_element_by_id("validate_weekly_weight").click()

        # check the element display
        message = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(message, "J'ai bien pris note de ton poids, "
                                  "tu trouveras un récapitulatif dans l'onglet résultats.")

        # new challenge
        self.browser.find_element_by_id("card").click()
        new_challenge = self.browser.find_element_by_id("dietetic_text").text
        self.assertNotEqual(new_challenge, old_challenge)

    def test_access_discussion_space_week_end_without_challenge(self):
        """
        test if the user clicks
        to the discussion space
        during the week-end and
        if the user have not challenges
        """
        # get user's data
        user_data = self.create_user_without_challenge()[1]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()

        # old challenge
        self.browser.find_element_by_id("card").click()
        old_challenge = self.browser.find_element_by_id("dietetic_text").text

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("85")
        self.browser.find_element_by_id("validate_weekly_weight").click()

        # new challenge
        self.browser.find_element_by_id("card").click()
        new_challenge = self.browser.find_element_by_id("dietetic_text").text
        self.assertNotEqual(new_challenge, old_challenge)

    def test_access_discussion_space_goal_achieved(self):
        """
        test if the user clicks
        to the discussion space
        during the week-end and
        write this weight goal
        """
        # get user's data
        user_data = self.create_user_one_week_ago()[1]

        # login user
        self.login_user(user_data)

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()

        # check the element display
        question = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(question, "Bonjour ! J'éspère que ta semaine s'est bien passée ? "
                                   "Que donne ta pesée ce matin ?")

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("50")
        self.browser.find_element_by_id("validate_weekly_weight").click()

        # check the element display
        message = self.browser.find_element_by_id("robot_comment").text
        self.assertEqual(message, 'Félicitation pseudo ! Tu as atteints ton objectif !')

        # check the button nav and card is display or not
        dict_nav = {"poll": self.assertFalse, "program": self.assertFalse,
                    "home": self.assertTrue, "user": self.assertTrue,
                    "clipboard": self.assertTrue, "card": self.assertFalse}
        for nav, method in dict_nav.items():
            try:
                self.browser.find_element_by_id(nav)
                nav_display = True
            except common.exceptions.NoSuchElementException:
                nav_display = False
            method(nav_display)
