#! /usr/bin/env python3
# coding: UTF-8

""" TestModel class """


# imports
from unittest import TestCase
from django.contrib.auth import get_user_model


class TestModel(TestCase):
    """ TestViews class :
    test_add_user method
    """

    def setUp(self):
        self.user = get_user_model()
        self.email = 'test@test2.com'
        self.password = 'testtest'
        self.id_user = 2

    def test_add_user(self):