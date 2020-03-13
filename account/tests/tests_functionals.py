#! /usr/bin/env python3
# coding: UTF-8

""" TestsFunctionals class """

# imports
import time
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser, StatusUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model, authenticate
from selenium import webdriver, common


class TestsFunctionals(StaticLiveServerTestCase):
    """ class TestsFunctionals :
    test the use user's account """

    def setUp(self):
        self.browser = webdriver.Firefox()

        # CREATE USER ACCOUNT 1
        self.user = get_user_model()
        self.dict_data_access_account = {"pseudo": "monpseudo", "id_email": "carole1@test.fr", "password": "00000000"}
        self.user_created = self.user.objects.create_user(username=self.dict_data_access_account.get('pseudo'),
                                                          email=self.dict_data_access_account.get('mail'),
                                                          password=self.dict_data_access_account.get('password'))

        # DATA TO CREATE USER ACCOUNT 2
        self.pseudo_create_account = "pseudotest"
        self.email_create_account = "carole2@test.fr"
        self.dict_data_create_account = {"pseudo": self.pseudo_create_account,
                                         "id_email": self.email_create_account,
                                         "password": self.dict_data_access_account.get('password')}

    def tearDown(self):
        self.browser.quit()

    def test_elements_display_home_page(self):
        """
        check the elements that display in the home page
        and the url retrieved if user clicks on login button
        or create account
        """
        self.browser.get(self.live_server_url + "/")

        # check the button nav is display or not
        dict_nav = {"poll": self.assertFalse, "program": self.assertFalse,
                    "home": self.assertFalse, "user": self.assertFalse,
                    "clipboard": self.assertFalse}
        for nav, method in dict_nav.items():
            try:
                nav = self.browser.find_element_by_id(nav)
                nav_display = True
            except common.exceptions.NoSuchElementException:
                nav_display = False
            method(nav_display)

        # url retrieved if user clicks on login button
        # or create account
        self.browser.find_element_by_id("create_account").click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + "/account/create_account/")
        self.browser.find_element_by_id("login").click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + "/account/login/")

    def test_create_account(self):
        """
        test create user's account
        and check the elements that display
        """
        self.browser.get(self.live_server_url + "/account/create_account/")

        # create user's account
        for key, value in self.dict_data_create_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check that user's account is created
        id = self.user.objects.values_list("id").get(email=self.email_create_account)
        is_active = StatusUser.objects.values_list("is_active").get(user=id)[0]
        self.assertTrue(is_active)

        # check that user is login
        user_authenticate = authenticate(email=self.email_create_account,
                                         password=self.dict_data_access_account.get('password'))
        self.assertNotEqual(user_authenticate, None)

        # check the text value that is display
        confirm_message = self.browser.find_element_by_id("confirm_message").text
        login_message = self.browser.find_element_by_id("login_message").text
        self.assertEqual(confirm_message, "Votre compte a bien été créé.")
        self.assertEqual(login_message, "Bonjour {} ! Vous êtes bien connecté.".format(self.pseudo_create_account))

        # check the button nav is display or not
        dict_nav = {"poll": self.assertFalse, "program": self.assertFalse,
                    "home": self.assertTrue, "user": self.assertTrue,
                    "clipboard": self.assertTrue}
        for nav, method in dict_nav.items():
            try:
                nav = self.browser.find_element_by_id(nav)
                nav_display = True
            except common.exceptions.NoSuchElementException:
                nav_display = False
            method(nav_display)

        def test_login_user(self):
            """ test login user in login page """
            self.browser.get(self.live_server_url + "/account/login/")

            # create user's account




