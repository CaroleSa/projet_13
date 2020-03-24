#! /usr/bin/env python3
# coding: UTF-8

""" TestsFunctionals class """

# imports
import time
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser, StatusUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model, authenticate
from django.test import Client
from selenium import webdriver, common


class TestsFunctionals(StaticLiveServerTestCase):
    """ class TestsFunctionals :
    test the use of the user's account """

    def setUp(self):
        self.browser = webdriver.Firefox()

        # CREATE USER ACCOUNT 1
        self.user = get_user_model()
        self.pseudo = "pseudo"
        self.dict_data_access_account = {"id_email": "carole1@test.fr", "id_password": "00000000"}
        self.user_created = self.user.objects.create_user(username=self.pseudo,
                                                          email=self.dict_data_access_account.get('id_email'),
                                                          password=self.dict_data_access_account.get('id_password'))
        HistoryUser.objects.create(user=self.user_created)
        StatusUser.objects.create(user=self.user_created)

        # DATA TO CREATE USER ACCOUNT 2
        self.pseudo_create_account = "pseudotest"
        self.email_create_account = "carole2@test.fr"
        self.dict_data_create_account = {"pseudo": self.pseudo_create_account,
                                         "id_email": self.email_create_account,
                                         "password": self.dict_data_access_account.get('id_password')}

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
        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()
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
                                         password=self.dict_data_access_account.get('id_password'))
        self.assertNotEqual(user_authenticate, None)

        # check the text value that is display
        confirm_message = self.browser.find_element_by_id("confirm_message").text
        login_message = self.browser.find_element_by_id("login_message").text
        self.assertEqual(confirm_message, "Votre compte a bien été créé.")
        self.assertEqual(login_message, "Bonjour {} ! Vous êtes bien connecté.".format(self.pseudo_create_account))

        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()

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

    def test_create_account_pseudo_error(self):
        """
        test create user's account
        with false pseudo
        """
        self.browser.get(self.live_server_url + "/account/create_account/")

        # create user's account with false pseudo
        self.dict_data_create_account["pseudo"] = "false pseudo"
        for key, value in self.dict_data_create_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error text value that is display
        error_message = self.browser.find_element_by_id("error_message_create").text
        self.assertEqual(error_message, "Pseudo non valide : peut contenir lettres "
                                        "ou chiffres, sans espace ni symbole.")

    def test_create_account_email_error(self):
        """
        test create user's account
        with false email
        """
        self.browser.get(self.live_server_url + "/account/create_account/")

        # create user's account with false email
        self.dict_data_create_account["id_email"] = "test@test.dr"
        for key, value in self.dict_data_create_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error text value that is display
        error_message = self.browser.find_element_by_id("error_message_create").text
        self.assertEqual(error_message, "Adresse e-mail non valide.")

    def test_create_account_password_error(self):
        """
        test create user's account
        with false password
        """
        self.browser.get(self.live_server_url + "/account/create_account/")

        # create user's account with false password
        self.dict_data_create_account["password"] = "    0000"
        for key, value in self.dict_data_create_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error text value that is display
        error_message = self.browser.find_element_by_id("error_message_create").text
        self.assertEqual(error_message, "Mot de passe non valide : peut contenir "
                                        "lettres, chiffres ou symboles $@%*+\-_! sans espace. "
                                        "Doit être composé de 8 caractères minimum.")

    def test_create_account_exists_email(self):
        """
        test create user's account
        with an exists email
        """
        self.browser.get(self.live_server_url + "/account/create_account/")

        # create user's account with false password
        self.dict_data_create_account["id_email"] = self.dict_data_access_account.get('id_email')
        for key, value in self.dict_data_create_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error text value that is display
        error_message = self.browser.find_element_by_id("error_message_create").text
        self.assertEqual(error_message, "Ce compte existe déjà.")

    def test_login_user(self):
        """ test login user in login page """
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the text value that is display
        login_message = self.browser.find_element_by_id("login_message").text
        self.assertEqual(login_message, "Bonjour {} ! Vous êtes bien connecté.".format(self.pseudo))

        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()

    def test_login_false_email(self):
        """ test login user with false email """
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        self.dict_data_access_account["id_email"] = "test@newmail.fr"
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error message value that is display
        login_message = self.browser.find_element_by_id("message_login").text
        self.assertEqual(login_message, "Ce compte n'existe pas.")

    def test_login_false_password(self):
        """ test login user with false password """
        self.browser.get(self.live_server_url + "/account/login/")

        # login user
        self.dict_data_access_account["id_password"] = "25469874"
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the error message value that is display
        login_message = self.browser.find_element_by_id("message_login").text
        self.assertEqual(login_message, "Le mot de passe est incorrect.")

    def test_access_my_account_page(self):
        """ test the access in user's account page """
        self.test_login_user()

        # access user's account page
        self.browser.find_element_by_id("user").click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + "/account/my_account/")

        # check the data value display
        title = self.browser.find_element_by_id("account_title").text
        pseudo = self.browser.find_element_by_id("pseudo_account").text
        mail = self.browser.find_element_by_id("mail_account").text
        self.assertEqual(title, "Mon compte")
        self.assertEqual(pseudo, "Pseudo : {}".format(self.pseudo))
        self.assertEqual(mail, "Adresse e-mail : {}".format(self.dict_data_access_account.get('id_email')))

    def test_edit_password(self):
        """ test edit user's password """
        self.test_login_user()
        self.browser.find_element_by_id("user").click()
        self.browser.find_element_by_id("key").click()

        # edit password
        new_password = "22222222"
        data_password = {"id_password": self.dict_data_access_account.get('id_password'),
                         "new_password": new_password}
        for key, value in data_password.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submit_password").click()

        # check the confirm message value
        confirm_message = self.browser.find_element_by_id("confirm").text
        self.assertEqual(confirm_message, "Votre mot de passe a bien été modifié.")

        # logout user
        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()
        self.browser.find_element_by_id("logout_account").click()
        # login user with the new password
        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()
        self.dict_data_access_account["id_password"] = new_password
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()

        # check the text value that is display
        login_message = self.browser.find_element_by_id("login_message").text
        self.assertEqual(login_message, "Bonjour {} ! Vous êtes bien connecté.".format(self.pseudo))

    def test_error_edit_password(self):
        """
        test edit user's password :
        display error messages
        """
        self.test_login_user()
        self.browser.find_element_by_id("user").click()
        self.browser.find_element_by_id("key").click()

        # edit password
        new_password = "22222222"
        data_password = {"id_password": "fauxpassword",
                         "new_password": new_password}
        for key, value in data_password.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submit_password").click()

        # check the error text value
        error_message = self.browser.find_element_by_id("error_actual").text
        self.assertEqual(error_message, "incorrect")

        # edit password
        data_password = {"id_password": self.dict_data_access_account.get('id_password'),
                         "new_password": "  222222"}
        for key, value in data_password.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submit_password").click()

        # check the error text value
        error_message = self.browser.find_element_by_id("error_new").text
        self.assertEqual(error_message, "invalide")

    def test_delete_account(self):
        """ test delete user's password """
        self.test_login_user()
        self.browser.find_element_by_id("user").click()

        # delete the user's account
        self.browser.find_element_by_id("delete_user").click()
        user_logo = self.browser.find_element_by_class_name("fa-user-circle")
        if user_logo:
            user_logo.click()
        message = self.browser.find_element_by_id("message_login").text
        self.assertEqual(message, "Votre compte a bien été supprimé.")

        # login user with account deleted
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()
        # check the text value that is display
        error_message = self.browser.find_element_by_id("message_login").text
        self.assertEqual(error_message, "Ce compte a été supprimé.")

        # create user's account with e-mail
        # of the account deleted
        self.browser.find_element_by_id("create_account").click()
        self.dict_data_access_account["pseudo"] = self.pseudo
        del self.dict_data_access_account["id_password"]
        self.dict_data_access_account["password"] = "00000000"
        for key, value in self.dict_data_access_account.items():
            self.browser.find_element_by_id(key).send_keys(value)
        self.browser.find_element_by_id("submitButton").click()
        # check the text value that is display
        error_message = self.browser.find_element_by_id("error_message_create").text
        self.assertEqual(error_message, "Ce compte a été supprimé et n'est pas réutilisable.")







