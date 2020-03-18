#! /usr/bin/env python3
# coding: UTF-8

""" TestDemo class """

# imports
import random
from datetime import date, timedelta
import time
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


class TestDemo(StaticLiveServerTestCase):
    """ class TestDemo """

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
            user_created = self.user.objects.create_user(id=id_user, username="Carole",
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
            user_created = self.user.objects.create_user(id=id_user, username="Carole",
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
            user_created = self.user.objects.create_user(id=id_user, username="Carole",
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
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        for key, value in dict_login.items():
            time.sleep(1)
            self.browser.find_element_by_id(key).send_keys(value)
        time.sleep(1)
        self.browser.find_element_by_id("submitButton").click()

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
        # login user
        for key, value in data_user.items():
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
        time.sleep(1)
        self.browser.find_element_by_id("validate_button").click()
        time.sleep(1)

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
        # login user
        data_user = self.create_user_4_days_ago()[1]
        self.login_user(data_user)

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(5)

        # check the elements display
        self.browser.find_element_by_id("card").click()
        time.sleep(5)

    def test_3_user_comes_week_end(self):
        """
        user is starting
        the challenge program
        and comes the week_end
        """
        # login user
        data_user = self.create_user_one_week_ago()[1]
        self.login_user(data_user)

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(5)

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("95")
        time.sleep(2)
        self.browser.find_element_by_id("validate_weekly_weight").click()
        time.sleep(5)

        # check challenge value
        self.browser.find_element_by_id("card").click()
        time.sleep(10)

        # check the results page
        self.browser.find_element_by_id("poll").click()
        time.sleep(10)

    def test_4_user_goal_achieved(self):
        """
        when the user has
        reached his goal
        """
        # login user
        data_user = self.create_user_one_week_ago()[1]
        self.login_user(data_user)

        # test access discussion space page
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(5)

        # check user writes this weekly weight
        self.browser.find_element_by_id("weekly_weight").send_keys("50")
        time.sleep(2)
        self.browser.find_element_by_id("validate_weekly_weight").click()
        time.sleep(5)

        # check discussion space value
        self.browser.find_element_by_id("clipboard").click()
        time.sleep(3)

