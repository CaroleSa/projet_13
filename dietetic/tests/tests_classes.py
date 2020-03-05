#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from unittest import TestCase
from ..classes.weight_advice_goal import WeightAdviceGoal


class TestsReturnWeightAdvicesGoal(TestCase):
    """ TestsClasses class """

    def setUp(self):
        self.new_weight_advice_goal = WeightAdviceGoal()

    def test_return_impossible_goal(self):
        actual_weight = 40
        cruising_weight = 38
        goal_weight = 38
        height = 1.55
        goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                      goal_weight, height)[0]
        self.assertEqual(goal, "impossible")

    def test_return_impossible_advice(self):
        actual_weight = 40
        cruising_weight = 38
        goal_weight = 38
        height = 1.55
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids."
        self.assertEqual(advice, text)

    def test_return_max_goal(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 38
        height = 1.50
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        height_min = 18.5 * (height * height)
        goal = actual_weight - height_min

        self.assertEqual(return_goal, goal)

    def test_return_max_advice(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 38
        height = 1.50
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[1]
        height_min = 18.5 * (height * height)
        text = "Ton objectif semble trop bas, je te conseille de ne pas " \
               "aller au dessous de"+str(height_min)+" kg."

        self.assertEqual(advice, text)

    def test_under_cruising_weight_goal(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 50
        height = 1.60
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        user_goal = actual_weight - goal_weight

        self.assertEqual(return_goal, user_goal)

    def test_under_cruising_weight_advice(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 50
        height = 1.60
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        text = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
               "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
               "aille en dessous de ce poids. Il est donc" \
               "possible que tu n'arrives pas à le maintenir sur la durée."

        self.assertEqual(advice, text)
