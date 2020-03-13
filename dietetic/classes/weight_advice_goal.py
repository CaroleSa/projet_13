#! /usr/bin/env python3
# coding: UTF-8

""" WeightAdviceGoal class """

# Imports
from dietetic.classes.calculation import Calculation


class WeightAdviceGoal:

    def __init__(self):
        self.new_calculation = Calculation()
        self.first_advice = ""
        self.final_weight = 0

    def return_weight_advices_goal(self, dict_data):
        """ get user's answer, return weight advice and goal """

        height = round(float(dict_data.get("height")), 2)
        actual_weight = round(float(dict_data.get("actual_weight")), 1)
        cruising_weight = round(float(dict_data.get("cruising_weight")), 1)
        goal_weight = round(float(dict_data.get("weight_goal")), 1)

        actual_imc = actual_weight/(height*height)
        goal_imc = goal_weight/(height*height)
        cruising_imc = cruising_weight/(height*height)

        user_goal = self.new_calculation.delete_o(actual_weight - goal_weight)

        if actual_imc < 18.5:
            advice = "Ton poids actuel est déjà bien bas... je te déconseille " \
                     "de perdre plus de poids. "
            goal = "impossible"
            final_weight = False

            return goal, advice, final_weight

        if goal_imc < 18.5:
            height_min = round(18.5*(height * height), 1)
            height_min = self.new_calculation.delete_o(height_min)
            advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                     "aller en dessous de "+str(height_min)+" kg. " \
                     "C'est donc l'objectif que nous allons fixer ! "
            goal = actual_weight - height_min
            final_weight = height_min

            return goal, advice, final_weight

        else:
            if cruising_imc < 23 and goal_weight < cruising_weight:
                advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                         "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                         "aille en dessous de ce poids. Je tiens donc à te préciser qu'il est" \
                         "possible que tu n'arrives pas à le maintenir sur la durée." \
                         "Je note tout de même cet objectif. "
            else:
                advice = "Alors c'est parti ! Partons sur un objectif " \
                         "de - " + str(user_goal) + " kg. "

            return user_goal, advice, goal_weight
