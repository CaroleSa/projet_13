#! /usr/bin/env python3
# coding: UTF-8

""" Calculation class """

# Imports
from account.models import ResultsUser, ProfileUser
# pylint: disable=no-member


class Calculation:
    """ Calculation class """

    def __init__(self):
        self.weighing_date = ResultsUser.objects.values_list("weighing_date")
        self.weight = ResultsUser.objects.values_list("weight")

    def create_results_data_list(self, user):
        """
        create a list that contains
        the user's results to display
        them in the graphic
        """
        # get data
        starting_date = self.weighing_date.filter(user=user).order_by("weighing_date").first()[0]
        results_date_data = self.weighing_date.filter(user=user).order_by("weighing_date")
        results_weight_data = self.weight.filter(user=user).order_by("weighing_date")

        # create a list
        list_data = [['Semaine', 'Poids']]
        for date, weight in zip(results_date_data, results_weight_data):
            delta = date[0] - starting_date
            number_of_weeks = round(delta.days / 7, 0)
            list_date_weight = [number_of_weeks, float(weight[0])]
            list_data.append(list_date_weight)

        return list_data

    def percentage_lost_weight(self, user):
        """
        calculates the percentage
        of weight lost by the user
        """
        # get data
        starting_weight = self.weight.filter(user=user).order_by("weighing_date").first()[0]
        last_weight = self.weight.filter(user=user).order_by("weighing_date").last()[0]
        final_weight = ProfileUser.objects.values_list("final_weight").get(user=user)[0]

        # calculation
        total_lost_weight = float(starting_weight - last_weight)
        total_goal = float(starting_weight - final_weight)
        lost_percentage = round(int((total_lost_weight * 100) / total_goal), 0)

        return lost_percentage

    def average_weight_loss(self, user):
        """
        calculates the average
        weight lost per week
        """
        # get data
        starting_date = self.weighing_date.filter(user=user).order_by("weighing_date").first()[0]
        last_date = self.weighing_date.filter(user=user).order_by("weighing_date").last()[0]
        starting_weight = self.weight.filter(user=user).order_by("weighing_date").first()[0]
        last_weight = self.weight.filter(user=user).order_by("weighing_date").last()[0]

        # calculation
        total_lost_weight = float(starting_weight - last_weight)
        delta = last_date - starting_date
        number_of_weeks = delta.days / 7
        try:
            average_lost_weight = round(total_lost_weight / number_of_weeks, 1)
        except ZeroDivisionError:
            average_lost_weight = 0

        return average_lost_weight

    @classmethod
    def delete_o(cls, float_number):
        """
        delete the 0 after
        the decimal point
        """
        int_number = int(float_number)
        if int_number == float_number:
            return int_number
        return float_number
