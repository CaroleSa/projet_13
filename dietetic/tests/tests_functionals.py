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
from django.test import Client
from selenium import webdriver, common
from datetime import datetime, timedelta
import calendar
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
'fr_FR'


class TestsFunctionals(StaticLiveServerTestCase):
    """ class TestsFunctionals :
    test the use of the dietetic challenge """

    fixtures = ['data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.question = ""

        # CREATE NEW USER
        self.user = get_user_model()
        self.pseudo = "pseudo"
        self.dict_data_access_account = {"id_email": "carole1@test.fr", "id_password": "00000000"}
        self.user_created = self.user.objects.create_user(username=self.pseudo,
                                                          email=self.dict_data_access_account.get('id_email'),
                                                          password=self.dict_data_access_account.get('id_password'))
        HistoryUser.objects.create(user=self.user_created)
        StatusUser.objects.create(user=self.user_created)

    def tearDown(self):
        self.browser.quit()

    def login_user(self):
        """ login user """
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

    def test_access_home_page(self):
        """
        test if the user clicks
        to the home nav
        """
        # login user
        self.login_user()

        # test access home page
        self.browser.find_element_by_id("home").click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/")

    def create_questions_id_list(self):
        """ create a list : robot questions
        by order discussion_space id """

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

        return id_question_by_type_list

    def test_questionnaire_answer_two_or_three(self):
        """
        test if the user choices
        the second and third answer
        to the first robot question
        """
        # login user
        self.login_user()

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
        # login user
        self.login_user()

        # access dietetic space page
        self.browser.find_element_by_id("clipboard").click()

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
        dict_data["height"] = 1.60
        advice = self.new_weight_advice_goal.return_weight_advices_goal(dict_data)[1]
        id_type = RobotQuestionType.objects.values_list("id").get(type="end start")[0]
        start_text_end = RobotQuestion.objects.values_list("text").get(robot_question_type=id_type)[0]
        text = advice + start_text_end

        robot_answer = self.browser.find_element_by_id("robot_answer").text
        self.assertEqual(text, robot_answer)

        """last_weighing_date = ResultsUser.objects.values_list("weighing_date").filter(user=id_user).last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        present = datetime.now()
        present_date = present.date()
        month = calendar.month_name[one_week_after_weighing.month]
        date = "" + calendar.day_name[one_week_after_weighing.weekday()] + " " + str(one_week_after_weighing.day) \
               + " " + month + ""
        robot_text = "Retrouvons nous ici {} pour faire le point sur tes prochains résultats " \
                     "et voir ton nouveau challenge !".format(date)"""

        """"# access my results page
        self.browser.find_element_by_id("poll").click()
        
        # check graphic is not display
        try:
            self.browser.find_element_by_id("graphic_my_results")
            graphic = True
        except common.exceptions.NoSuchElementException:
            graphic = False
        self.assertFalse(graphic)
        
        # check values data display"""
