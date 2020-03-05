#! /usr/bin/env python3
# coding: UTF-8

""" WeightAdviceGoal class """

# Imports


class WeightAdviceGoal:

    def return_weight_advices_goal(self, actual_weight, cruising_weight, goal_weight, height):
        """ get user's answer, return weight advice and goal """

        actual_imc = round(actual_weight/(height*height), 1)
        goal_imc = round(goal_weight/(height*height), 1)
        cruising_imc = round(cruising_weight/(height*height), 1)

        user_goal = actual_weight - goal_weight

        if actual_imc < 18.5:
            advice = "Ton poids actuel est déjà bien bas... je te déconseille " \
                     "de perdre plus de poids."
            goal = "impossible"
            return goal, advice

        if goal_imc < 18.5:
            height_min = 18.5*(height * height)
            advice = "Ton objectif semble trop bas, je te conseille de ne pas " \
                     "aller en dessous de"+str(height_min)+" kg. Ça sera ton objectif !"
            goal = actual_weight - height_min
            return goal, advice

        if cruising_imc < 23 and goal_weight < cruising_weight:
            advice = "Chaque personne a un poids d'équilibre sur lequel il peut rester longtemps, " \
                     "c'est se qu'on appelle le poids de croisière. Il semble que ton objectif " \
                     "aille en dessous de ce poids. Il est donc" \
                     "possible que tu n'arrives pas à le maintenir sur la durée."
            goal = user_goal
            return goal, advice

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

            advice = "Prévoir un objectif rapidement atteignable est une bonne chose pour rester motiver." \
                     "Je te propose donc de prévoir un premier objectif puis un second, ..."+advice+""
            return goal, advice

        else:
            advice = "Alors c'est parti ! Partons sur un objectif de - " \
                    + str(user_goal) + " kg. Passons maintenant à la suite du questionnaire."
            goal = user_goal
            return goal, advice
