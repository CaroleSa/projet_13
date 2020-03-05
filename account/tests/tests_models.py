#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from account.models import ResultsUser, ProfileUser, HistoryUser, StatusUser, IdentityUser
from datetime import date
import re


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    def setUp(self):
        # get custom user model
        self.user = get_user_model()

        # data for test_add_user method
        self.username1 = 'pseudo1'
        self.email1 = 'pseudo1@tests.com'
        self.password1 = 'password1'
        self.id_user1 = 1

        # create user account
        self.username2 = 'pseudo2'
        self.email2 = 'pseudo2@tests.com'
        self.password2 = 'password2'
        self.id_user2 = 2
        try:
            self.user.objects.create_user(id=self.id_user2, username=self.username2, email=self.email2,
                                          password=self.password2)
        except IntegrityError:
            pass

        self.user_created = self.user.objects.get(id=self.id_user2)

    def test_add_user(self):
        """ Test create user account """
        try:
            user_created = self.user.objects.create_user(id=self.id_user1, username=self.username1, email=self.email1,
                                                         password=self.password1)
        except IntegrityError:
            pass
        self.assertIn(self.username1, str(user_created))

    def test_get_user_created(self):
        """ Test get account user created or not created """
        # try to get the data from an existing user (id = 2)
        # and from an nonexistent user (id = 5)
        dict_id_method = {self.id_user2: self.assertTrue, '5': self.assertFalse}
        for id_user, method in dict_id_method.items():
            try:
                self.user.objects.get(id=id_user)
                get_user = True
            except self.user.DoesNotExist:
                get_user = False
            method(get_user)

    def test_get_data_user_created(self):
        """ Test get data user created """
        data = self.user.objects.values_list('email')
        email = data.get(username=self.username2)[0]
        self.assertEqual(email, self.email2)

    def test_user_deactivate(self):
        """ Test user deactivate """
        user = self.user.objects.get(id=self.id_user2)
        user.is_active = False
        user.save()
        self.assertFalse(user.is_active)

    def test_add_get_profile_user(self):
        """ Test create user profile and get data """
        starting_weight = 100
        final_weight = 80
        try:
            ProfileUser.objects.create(user=self.user_created, starting_weight=starting_weight,
                                       final_weight=final_weight)
        except IntegrityError:
            pass
        data = ProfileUser.objects.values_list('starting_weight')
        get_weight_user = data.get(user=self.user_created)
        self.assertEqual(get_weight_user[0], starting_weight)

    def test_add_get_results_user(self):
        """ Test create user results and get results """
        weight = 55.0
        date = "2020-5-20"
        try:
            ResultsUser.objects.create(user=self.user_created, weighing_date=date, weight=weight)
        except IntegrityError:
            pass
        data = ResultsUser.objects.values_list('weight').filter(weighing_date=date)
        get_weight_user = data.get(user=self.user_created)
        self.assertEqual(get_weight_user[0], weight)

        data = ResultsUser.objects.values_list('weighing_date').filter(weight=weight)
        date_data = data.get(user=self.user_created)
        date_data_list = re.findall('\d+', str(date_data))
        date_weight = ""+date_data_list[0]+"-"+date_data_list[1]+"-"+date_data_list[2]+""
        self.assertEqual(date_weight, date)

    def test_add_get_history_user(self):
        """ Test add and get user's history data """
        try:
            HistoryUser.objects.create(user=self.user_created)
        except IntegrityError:
            pass
        date_data = HistoryUser.objects.values_list("date_joined").get(user=self.user_created)
        date_create_account_list = re.findall('\d+', str(date_data))[0:3]
        today = date.today()
        today_list = [str(today.year), str(today.month), str(today.day)]
        self.assertEqual(date_create_account_list, today_list)
