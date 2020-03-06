#! /usr/bin/env python3
# coding: UTF-8

""" WeightAdviceGoal class """

# Imports


class WeightAdviceGoal:

    def __init__(self):
        self.first_advice = ""
        self.final_weight = 0

    def return_weight_advices_goal(self, dict_data):
        """ get user's answer, return weight advice and goal """

        height = float(dict_data.get("height"))
        actual_weight = float(dict_data.get("actual_weight"))
        cruising_weight = float(dict_data.get("cruising_weight"))
        goal_weight = float(dict_data.get("weight_goal"))

        actual_imc = round(actual_weight/(height*height), 1)
        goal_imc = round(goal_weight/(height*height), 1)
        cruising_imc = round(cruising_weight/(height*height), 1)

        user_goal = actual_weight - goal_weight

        if actual_imc < 18.5:
            advice = "Ton poids actuel est déjà bien bas... je te déconseille " \
                     "de perdre plus de poids."
            goal = "impossible"
            self.final_weight = False

            return goal, advice, self.final_weight

        if goal_imc < 18.5:
            height_min = 18.5*(height * height)
            self.first_advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                                "aller en dessous de"+str(height_min)+" kg."
            user_goal = actual_weight - height_min
            self.final_weight = round(height_min, 1)

        else:
            if cruising_imc < 23 and goal_weight < cruising_weight:
                self.first_advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                        "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                        "aille en dessous de ce poids. Il est donc" \
                        "possible que tu n'arrives pas à le maintenir sur la durée."
                self.final_weight = goal_weight

        if user_goal > 6:
            second_goal = user_goal-6

            if second_goal <= 3:
                actual_goal = user_goal/2
                advice = "Ton premier objectif serra donc de perdre "+str(actual_goal)+" kg. " \
                         "C'est parti ! Passons maintenant à la suite du questionnaire."
                goal = actual_goal

            else:
                advice = "Ton premier objectif serra donc de perdre 5 kg. C'est parti ! " \
                        "Passons maintenant à la suite du questionnaire."
                goal = 5

            if self.first_advice:
                advice = ""+self.first_advice+"Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                         "Je te propose donc de prévoir un premier objectif puis un second, ..."+advice+" "

            else:
                advice = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                         "Je te propose donc de prévoir un premier objectif puis un second, ..." + advice + " "

        else:
            advice = "Alors c'est parti ! Partons sur un objectif de - " \
                    + str(user_goal) + " kg. "
            goal = user_goal
            self.final_weight = goal_weight

        return goal, advice, self.final_weight
