#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from unittest import TestCase
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.models import DiscussionSpace


class TestsReturnWeightAdvicesGoal(TestCase):
    """ TestsReturnWeightAdvicesGoal class """

    def setUp(self):
        self.new_weight_advice_goal = WeightAdviceGoal()

    def test_return_goal_impossible_goal(self):
        actual_weight = 40
        cruising_weight = 38
        goal_weight = 38
        height = 1.55
        goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                      goal_weight, height)[0]
        self.assertEqual(goal, "impossible")

    def test_return_advice_impossible_goal(self):
        actual_weight = 40
        cruising_weight = 38
        goal_weight = 38
        height = 1.55
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids."
        self.assertEqual(advice, text)

    def test_return_goal_min_weight(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 38
        height = 1.50
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        height_min = 18.5 * (height * height)
        goal = actual_weight - height_min

        self.assertEqual(return_goal, goal)

    def test_return_advice_min_weight(self):
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

    def test_return_goal_under_cruising_weight(self):
        actual_weight = 60
        cruising_weight = 55
        goal_weight = 50
        height = 1.60
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        user_goal = actual_weight - goal_weight

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_under_cruising_weight(self):
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

    def test_return_goal_goal_under_6_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 66
        height = 1.60
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        user_goal = actual_weight - goal_weight

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_goal_under_6_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 66
        height = 1.60
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        user_goal = actual_weight - goal_weight
        text = "Alors c'est parti ! Partons sur un objectif de - " \
               + str(user_goal) + " kg. Passons maintenant à la suite du questionnaire."

        self.assertEqual(advice, text)

    def test_return_goal_goal_above_6_kg_second_goal_under_3_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 63
        height = 1.60
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        user_goal = actual_weight - goal_weight
        actual_goal = user_goal / 2

        self.assertEqual(return_goal, actual_goal)

    def test_return_advice_goal_above_6_kg_second_goal_under_3_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 63
        height = 1.60
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        user_goal = actual_weight - goal_weight
        actual_goal = user_goal / 2
        text = "Ton premier objectif serra donc de perdre "+str(actual_goal)+\
               " kg. C'est parti ! Passons maintenant à la suite du questionnaire."
        text = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                "Je te propose donc de prévoir un premier objectif puis un second, ..." + text + ""

        self.assertEqual(advice, text)

    def test_return_goal_goal_above_6_kg_second_goal_above_3_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 60
        height = 1.60
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                             goal_weight, height)[0]
        self.assertEqual(return_goal, 5)

    def test_return_advice_goal_above_6_kg_second_goal_above_3_kg(self):
        actual_weight = 70
        cruising_weight = 55
        goal_weight = 60
        height = 1.60
        advice = self.new_weight_advice_goal.return_weight_advices_goal(actual_weight, cruising_weight,
                                                                        goal_weight, height)[1]
        text = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
               "Passons maintenant à la suite du questionnaire."
        text = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                "Je te propose donc de prévoir un premier objectif puis un second, ..." + text + ""

        self.assertEqual(advice, text)


class TestsReturnQuestionsList(TestCase):
    """ TestsReturnQuestionsList class """

    def setUp(self):
        self.new_questions_list = QuestionsList()

    def test_return_questions_list(self):
        data = DiscussionSpace.objects.values_list("robot_question").order_by("id")
        list_data = []
        for elt in data:
            list_data.append(elt[0])
        new_list = []
        for i in list_data:
            if i not in new_list:
                new_list.append(i)

        return_list = self.new_questions_list.create_questions_id_list()

        self.assertEqual(new_list, return_list)
