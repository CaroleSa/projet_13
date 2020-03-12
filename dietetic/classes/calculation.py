#! /usr/bin/env python3
# coding: UTF-8

""" Calculation class """

# Imports
from account.models import ResultsUser, ProfileUser


class Calculation:

    def create_results_data_list(self, id):
        results_weight_data = ResultsUser.objects.values_list("weight").filter(user=id).order_by("weighing_date")
        results_date_data = ResultsUser.objects.values_list("weighing_date").filter(user=id).order_by("weighing_date")

        list_data = [['Date', 'Poids']]
        for date, weight in zip(results_date_data, results_weight_data):
            list_date_weight = [date[0], float(weight[0])]
            list_data.append(list_date_weight)

        return list_data

    def percentage_lost_weight(self, id):
        starting_weight = ResultsUser.objects.values_list("weight").filter(user=id).first()[0]
        last_weight = ResultsUser.objects.values_list("weight").filter(user=id).last()[0]
        final_weight = ProfileUser.objects.values_list("final_weight").get(user=id)[0]

        total_lost_weight = float(starting_weight - last_weight)
        total_goal = float(starting_weight - final_weight)
        lost_percentage = round(int((total_lost_weight * 100) / total_goal), 0)

        return lost_percentage

    def average_weight_loss(self, id):
        # calculates the average weight loss
        starting_date = ResultsUser.objects.values_list("weighing_date").filter(user=id).first()[0]
        last_date = ResultsUser.objects.values_list("weighing_date").filter(user=id).last()[0]
        starting_weight = ResultsUser.objects.values_list("weight").filter(user=id).first()[0]
        last_weight = ResultsUser.objects.values_list("weight").filter(user=id).last()[0]

        total_lost_weight = float(starting_weight - last_weight)
        delta = last_date - starting_date
        number_of_weeks = delta.days / 7
        try:
            average_lost_weight = round(total_lost_weight / number_of_weeks, 1)
        except ZeroDivisionError:
            average_lost_weight = 0

        return average_lost_weight
