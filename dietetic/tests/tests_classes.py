#! /usr/bin/env python3
# coding: UTF-8

""" TestsClasses class """

# imports
from unittest import TestCase
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from dietetic.classes.questions_list import QuestionsList
from dietetic.models import DiscussionSpace, RobotQuestion


class TestsReturnWeightAdvicesGoal(TestCase):
    """ TestsReturnWeightAdvicesGoal class """

    def setUp(self):
        self.new_weight_advice_goal = WeightAdviceGoal()

    def test_return_goal_under_cruising_weight(self):
        """
        test goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 50}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(return_goal, 5)

    def test_return_advice_under_cruising_weight(self):
        """
        test advice returned if the user's weight goal
         is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 50}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        first_advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                       "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                       "aille en dessous de ce poids. Il est donc" \
                       "possible que tu n'arrives pas à le maintenir sur la durée."
        advice = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
                 "Passons maintenant à la suite du questionnaire."
        text = ""+first_advice+"Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
               "Je te propose donc de prévoir un premier objectif puis un second, ..." + advice + " "

        self.assertEqual(return_advice, text)

    def test_return_goal_weight_under_cruising_weight(self):
        """
        test weight goal returned if the user's weight goal
        is under to this cruising weight
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 50}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        weight_goal = data_weight_user["weight_goal"]

        self.assertEqual(return_goal, weight_goal)

    def test_return_goal_actual_weight_is_too_low(self):
        """
        test goal returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        user_goal = "impossible"

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_actual_weight_is_too_low(self):
        """
        test advice returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids."

        self.assertEqual(advice, text)

    def test_return_goal_weight_actual_weight_is_too_low(self):
        """
        test goal weight returned if the user's actual weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 45,
                            "cruising_weight": 45, "weight_goal": 40}
        goal_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

        self.assertEqual(goal_weight, False)

    def test_return_goal_goal_weight_is_too_low(self):
        """
        test goal returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(return_goal, 5)

    def test_return_advice_goal_weight_is_too_low(self):
        """
        test advice returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        height = data_weight_user["height"]
        height_min = 18.5 * (height * height)
        first_advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                            "aller en dessous de" + str(height_min) + " kg."
        advice = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
                 "Passons maintenant à la suite du questionnaire."
        text = "" + first_advice + "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                                   "Je te propose donc de prévoir un premier objectif puis un second, ..." + advice + " "

        self.assertEqual(return_advice, text)

    def test_return_goal_weight_goal_weight_is_too_low(self):
        """
        test goal weight returned if the user's goal weight
        is too low
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 45, "weight_goal": 40}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]
        height = data_weight_user["height"]
        height_min = 18.5 * (height * height)
        height_min = round(height_min, 1)

        self.assertEqual(return_goal, height_min)

    def test_return_goal_goal_weight_under_6_kg(self):
        """
        test goal returned if the user's goal weight
        is under to 6 kg
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 55}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        actual_weight = data_weight_user["actual_weight"]
        weight_goal = data_weight_user["weight_goal"]
        goal = actual_weight - weight_goal

        self.assertEqual(return_goal, goal)

    def test_return_advice_goal_weight_under_6_kg(self):
        """
        test advice returned if the user's goal weight
        is under to 6 kg
        """
        data_weight_user = {"height": 1.60, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 55}
        return_advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]

        actual_weight = data_weight_user["actual_weight"]
        weight_goal = data_weight_user["weight_goal"]
        user_goal = float(actual_weight - weight_goal)
        advice = "Alors c'est parti ! Partons sur un objectif de - " \
                 + str(user_goal) + " kg. "

        self.assertEqual(return_advice, advice)








    """def test_return_goal_impossible_goal(self):
        data_weight_user = {"height": 1.55, "actual_weight": 40,
                            "cruising_weight": 38, "weight_goal": 38}
        goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(goal, "impossible")

    def test_return_advice_impossible_goal(self):
        data_weight_user = {"height": 1.55, "actual_weight": 40,
                            "cruising_weight": 38, "weight_goal": 38}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]
        text = "Ton poids actuel est déjà bien bas... je te déconseille " \
               "de perdre plus de poids."

        self.assertEqual(advice, text)

    def test_return_goal_min_weight(self):
        data_weight_user = {"height": 1.50, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 38}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]
        height = data_weight_user["height"]
        actual_weight = data_weight_user["actual_weight"]
        height_min = 18.5 * (height * height)
        goal = actual_weight - height_min

        self.assertEqual(return_goal, goal)

    def test_return_advice_min_weight(self):
        data_weight_user = {"height": 1.50, "actual_weight": 60,
                            "cruising_weight": 55, "weight_goal": 38}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]
        height = data_weight_user["height"]
        height_min = 18.5 * (height * height)
        text = "Ton objectif semble trop bas, je te conseille de ne pas " \
               "aller en dessous de"+str(height_min)+" kg. Ça sera ton objectif !"

        self.assertEqual(advice, text)



    def test_return_goal_goal_under_6_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 66}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]
        actual_weight = data_weight_user["actual_weight"]
        goal_weight = data_weight_user["weight_goal"]
        user_goal = actual_weight - goal_weight

        self.assertEqual(return_goal, user_goal)

    def test_return_advice_goal_under_6_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 66}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]
        actual_weight = data_weight_user["actual_weight"]
        goal_weight = data_weight_user["weight_goal"]
        user_goal = actual_weight - goal_weight
        text = "Alors c'est parti ! Partons sur un objectif de - " \
               + str(user_goal) + " kg. Passons maintenant à la suite du questionnaire."

        self.assertEqual(advice, text)

    def test_return_goal_goal_above_6_kg_second_goal_under_3_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 63}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]
        actual_weight = data_weight_user["actual_weight"]
        goal_weight = data_weight_user["weight_goal"]
        user_goal = actual_weight - goal_weight
        actual_goal = user_goal / 2

        self.assertEqual(return_goal, actual_goal)

    def test_return_advice_goal_above_6_kg_second_goal_under_3_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 63}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]
        actual_weight = data_weight_user["actual_weight"]
        goal_weight = data_weight_user["weight_goal"]
        user_goal = actual_weight - goal_weight
        actual_goal = user_goal / 2
        text = "Ton premier objectif serra donc de perdre "+str(actual_goal)+\
               " kg. C'est parti ! Passons maintenant à la suite du questionnaire."
        text = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                "Je te propose donc de prévoir un premier objectif puis un second, ..." + text + ""

        self.assertEqual(advice, text)

    def test_return_goal_goal_above_6_kg_second_goal_above_3_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 60}
        return_goal = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]

        self.assertEqual(return_goal, 5)

    def test_return_advice_goal_above_6_kg_second_goal_above_3_kg(self):
        data_weight_user = {"height": 1.60, "actual_weight": 70,
                            "cruising_weight": 55, "weight_goal": 60}
        advice = self.new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]
        text = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
               "Passons maintenant à la suite du questionnaire."
        text = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
               "Je te propose donc de prévoir un premier objectif puis un second, ..." + text + ""

        self.assertEqual(advice, text)"""


class TestsReturnQuestionsList(TestCase):
    """ TestsReturnQuestionsList class """

    def setUp(self):
        self.new_questions_list = QuestionsList()

    def test_return_questions_list(self):
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

        return_list = self.new_questions_list.create_questions_id_list()

        self.assertEqual(id_question_by_type_list, return_list)
