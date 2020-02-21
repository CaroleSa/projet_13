#! /usr/bin/env python3
# coding: UTF-8

""" TestsModels class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from account.models import ResultsUser, ProfileUser


class TestsModels(TestCase):
    """ TestsModels class :
    test_add_user method
    """

    def setUp(self):
        # get custom user model
        self.user = get_user_model()

        # delete all data in database
        models_list = [self.user]
        for table in models_list:
            table.objects.all().delete()

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
        self.user.objects.create_user(id=self.id_user2, username=self.username2, email=self.email2,
                                      password=self.password2)
        self.user_created = self.user.objects.get(id=self.id_user2)

    def test_add_user(self):
        """ Test create user account """
        user_created = self.user.objects.create_user(id=self.id_user1, username=self.username1, email=self.email1,
                                                     password=self.password1)
        self.assertIn(str(user_created), self.username1)

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
        ProfileUser.objects.create(user=self.user_created, starting_weight=starting_weight, final_weight=final_weight)
        data = ProfileUser.objects.values_list('starting_weight')
        get_weight_user = data.get(user=self.user_created)
        self.assertEqual(get_weight_user[0], starting_weight)

    def test_add_get_results_user(self):
        """ Test create user results and get results """
        weight = 55.0
        date = "2020-05-20"
        ResultsUser.objects.create(user=self.user_created, weighing_date=date, weight=weight)
        data = ResultsUser.objects.values_list('weight').filter(weighing_date=date)
        get_weight_user = data.get(user=self.user_created)
        self.assertEqual(get_weight_user[0], weight)
