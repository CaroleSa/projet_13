#! /usr/bin/env python3
# coding: UTF-8

""" TestsFunctionals class """

# imports
import random
import time
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser, StatusUser
from dietetic.models import DiscussionSpace, RobotQuestionType, RobotQuestion, UserAnswer
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model, authenticate
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from django.db import connection
from selenium import webdriver, common
from datetime import date, timedelta
from psycopg2.errors import UniqueViolation
from django.db.utils import IntegrityError
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
'fr_FR'


class TestDemo(StaticLiveServerTestCase):
    """ class TestDemo :
    test the use of the dietetic challenge """

    fixtures = ['data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.cursor = connection.cursor()
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.question = ""

        # CREATE A NEW USER
        self.user = get_user_model()
        self.pseudo = "pseudo"
        id_user = 1
        self.dict_data_new_user = {"id_email": "carole1@test.fr", "id_password": "00000000"}
        self.new_user_created = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                              email=self.dict_data_new_user.get('id_email'),
                                                              password=self.dict_data_new_user.get('id_password'))
        HistoryUser.objects.create(user=self.new_user_created)
        StatusUser.objects.create(user=self.new_user_created)

        # CREATE A USER THAT IS STARTING PROGRAM
        self.dict_data_start_user = {"id_email": "carole2@test.fr", "id_password": "00000000"}
        id_user = 2
        self.start_user_created = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                                email=self.dict_data_start_user.get('id_email'),
                                                                password=self.dict_data_start_user.get('id_password'))
        HistoryUser.objects.create(user=self.start_user_created)
        StatusUser.objects.create(user=self.start_user_created)
        ProfileUser.objects.create(user=self.start_user_created, starting_weight=100,
                                   actual_goal_weight=50, final_weight=50)
        ResultsUser.objects.create(user=self.start_user_created, weight=100)
        user = HistoryUser.objects.get(user=self.start_user_created)
        user.start_questionnaire_completed = True
        user.save()
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 1))

        # CREATE A USER A WEEK AGO
        self.dict_data_user_a_week_ago = {"id_email": "carole3@test.fr", "id_password": "00000000"}
        id_user = 3
        self.user_create_a_week_ago = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                                   email=self.dict_data_user_a_week_ago.get('id_email'),
                                                                   password=self.dict_data_user_a_week_ago.get('id_password'))
        HistoryUser.objects.create(user=self.user_create_a_week_ago)
        StatusUser.objects.create(user=self.user_create_a_week_ago)
        ProfileUser.objects.create(user=self.user_create_a_week_ago, starting_weight=100,
                                   actual_goal_weight=50, final_weight=50)
        one_week_before = date.today() - timedelta(days=7)
        ResultsUser.objects.create(user=self.user_create_a_week_ago, weighing_date=one_week_before, weight=100)
        user = HistoryUser.objects.get(user=self.user_create_a_week_ago)
        user.start_questionnaire_completed = True
        user.save()
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 1))
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 4))

        # CREATE A USER WITHOUT CHALLENGES
        self.dict_data_user_without_challenge = {"id_email": "carole4@test.fr", "id_password": "00000000"}
        id_user = 4
        self.user_create_without_challenge = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                                    email=self.dict_data_user_without_challenge.get(
                                                                        'id_email'),
                                                                    password=self.dict_data_user_without_challenge.get(
                                                                        'id_password'))
        HistoryUser.objects.create(user=self.user_create_without_challenge)
        StatusUser.objects.create(user=self.user_create_without_challenge)
        ProfileUser.objects.create(user=self.user_create_without_challenge, starting_weight=100,
                                   actual_goal_weight=50, final_weight=50)
        one_week_before = date.today() - timedelta(days=7)
        ResultsUser.objects.create(user=self.user_create_without_challenge, weighing_date=one_week_before, weight=100)
        user = HistoryUser.objects.get(user=self.user_create_without_challenge)
        user.start_questionnaire_completed = True
        user.save()
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 1))

        # CREATE A USER
        # who has been following the program for 2 weeks
        self.dict_data_user_two_weeks = {"id_email": "carole5@test.fr", "id_password": "00000000"}
        id_user = 5
        self.user_create_two_weeks = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                                           email=self.dict_data_user_two_weeks.get(
                                                                               'id_email'),
                                                                           password=self.dict_data_user_two_weeks.get(
                                                                               'id_password'))
        HistoryUser.objects.create(user=self.user_create_two_weeks)
        StatusUser.objects.create(user=self.user_create_two_weeks)
        ProfileUser.objects.create(user=self.user_create_two_weeks, starting_weight=100,
                                   actual_goal_weight=50, final_weight=50)
        one_week_before = date.today() - timedelta(days=7)
        ResultsUser.objects.create(user=self.user_create_two_weeks, weighing_date=one_week_before, weight=100)
        ResultsUser.objects.create(user=self.user_create_two_weeks, weighing_date=date.today(), weight=95)
        user = HistoryUser.objects.get(user=self.user_create_two_weeks)
        user.start_questionnaire_completed = True
        user.save()
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 1))

        # CREATE A USER
        # who reached his weight goal
        self.dict_data_user_goal_ok = {"id_email": "carole6@test.fr", "id_password": "00000000"}
        id_user = 6
        self.user_create_goal_ok = self.user.objects.create_user(id=id_user, username=self.pseudo,
                                                                   email=self.dict_data_user_goal_ok.get(
                                                                       'id_email'),
                                                                   password=self.dict_data_user_goal_ok.get(
                                                                       'id_password'))
        HistoryUser.objects.create(user=self.user_create_goal_ok)
        StatusUser.objects.create(user=self.user_create_goal_ok)
        ProfileUser.objects.create(user=self.user_create_goal_ok, starting_weight=100,
                                   actual_goal_weight=5, final_weight=95)
        one_week_before = date.today() - timedelta(days=7)
        ResultsUser.objects.create(user=self.user_create_goal_ok, weighing_date=one_week_before, weight=100)
        user = HistoryUser.objects.get(user=self.user_create_goal_ok)
        user.start_questionnaire_completed = True
        user.save()
        ResultsUser.objects.create(user=self.user_create_goal_ok, weighing_date=date.today(), weight=95)
        self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                            "VALUES ({}, {})".format(id_user, 1))

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

    def create_user_4_days_ago(self):
        """
            create a user
            who has been following
            the program for 4 days
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
            one_week_before = date.today() - timedelta(days=4)
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

    def login_user(self, dict_login):
        """ login user """

    def test_1_user_access_account(self):
        """
        the user accesses
        to the account page
        """
        # login and create account user
        self.browser.get(self.live_server_url + "/account/login/")
        time.sleep(5)
        self.browser.find_element_by_id("create_account").click()
        time.sleep(3)
        self.browser.find_element_by_id("login").click()
        time.sleep(2)

        # login user
        data_user = self.create_user_not_start_program()[1]
        for key, value in data_user:
            time.sleep(1)
            self.browser.find_element_by_id(key).send_keys(value)
        time.sleep(1)
        self.browser.find_element_by_id("submitButton").click()

        # test access user page
        self.browser.find_element_by_id("user").click()
        time.sleep(3)
        self.browser.find_element_by_id("key").click()
        time.sleep(3)

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(3)

        # first answer to the first robot question
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
                    DiscussionSpace.objects.values_list("user_answer").filter(robot_question=id_robot_question)[number][
                        0]
                user_answer_text = UserAnswer.objects.values_list("text").get(id=user_answer_id)[0]
                self.browser.find_element_by_id(user_answer_text).click()
                self.browser.find_element_by_id("validate_button").click()
                time.sleep(1)
            except common.exceptions.NoSuchElementException:
                break

        # user writes this goal weight, ...
        dict_data = {"height": "1,60", "actual_weight": "60", "cruising_weight": "50", "weight_goal": "50"}
        for key, value in dict_data.items():
            time.sleep(1)
            self.browser.find_element_by_id(key).send_keys(value)
        time.sleep(1)
        self.browser.find_element_by_id("validate_goal").click()
        time.sleep(10)

        # check the elements display
        self.browser.find_element_by_id("card").click()
        time.sleep(5)
        self.browser.find_element_by_id("poll").click()
        time.sleep(10)
        self.browser.find_element_by_id("program").click()
        time.sleep(5)

    def test_2_user_comes_midweek(self):
        """
        user is starting
        the challenge program
        and comes to midweek
        """
        # access login page
        self.browser.get(self.live_server_url + "/account/login/")
        time.sleep(5)

        # login user
        data_user = self.create_user_4_days_ago()[1]
        for key, value in data_user:
            time.sleep(1)
            self.browser.find_element_by_id(key).send_keys(value)
        time.sleep(1)
        self.browser.find_element_by_id("submitButton").click()

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(5)

        # check the elements display
        self.browser.find_element_by_id("card").click()
        time.sleep(5)

    def test_2_user_comes_week_end(self):
        """
        user is starting
        the challenge program
        and comes the week_end
        """
        # access login page
        self.browser.get(self.live_server_url + "/account/login/")
        time.sleep(5)

        # login user
        data_user = self.create_user_one_week_ago()[1]
        for key, value in data_user:
            time.sleep(1)
            self.browser.find_element_by_id(key).send_keys(value)
        time.sleep(1)
        self.browser.find_element_by_id("submitButton").click()

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(5)

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("95")
        time.sleep(2)
        self.browser.find_element_by_id("validate_weekly_weight").click()
        time.sleep(5)

        self.browser.find_element_by_id("card").click()
        time.sleep(10)

