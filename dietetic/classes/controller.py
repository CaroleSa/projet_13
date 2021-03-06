#! /usr/bin/env python3
# coding: UTF-8

""" Controller class """

# Imports
import calendar
import locale
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from account.models import HistoryUser, ProfileUser, ResultsUser, \
    AdvicesToUser
from dietetic.models import RobotAdvices, DiscussionSpace, RobotQuestion, \
    RobotQuestionType, UserAnswer, RobotAdviceType
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
# pylint: disable=no-member


class Controller:
    """ Controller class """

    def __init__(self):
        self.new_questions_list = QuestionsList()
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.user = get_user_model()
        self.new_week = False
        self.end_questions_start = False
        self.end = False
        self.dict_questions = {"height": "Quelle taille fais-tu ? (au format x,xx)",
                               "actual_weight": "Quel est ton poids actuel ?",
                               "cruising_weight": "Quel est ton poids de croisière "
                                                  "(poids le plus longtemps "
                                                  "maintenu sans effort) ?",
                               "weight_goal": "Quel est ton poids d'objectif ?"}
        self.goal_text = "Nous allons maintenant définir ton objectif."

    def controller_dietetic_space_view(self, id_user, old_robot_question, data_weight_user,
                                       user_answer, weekly_weight):
        """
        controller
        to the discussion
        space view
        """
        # get data
        start_questionnaire_completed = HistoryUser.objects\
            .values_list("start_questionnaire_completed")
        start_questionnaire_completed = start_questionnaire_completed.get(user=id_user)[0]
        user = self.user.objects.get(id=id_user)
        advice_to_user = user.advices_to_user.all().count()
        context = {}

        # if the user have not answered
        # the start questions
        if start_questionnaire_completed is False:

            # return start discussion text
            # and save first user's data
            context = self.return_start_discussion(id_user, old_robot_question,
                                                   data_weight_user, user_answer)

        # if the user have answered
        # the start questions
        if start_questionnaire_completed is True or self.end_questions_start is True:

            # return weekly question
            # and save new weight
            if context != {}:
                context_2 = self.return_weekly_questions_save_weight(weekly_weight, id_user)
                context.update(context_2)
            else:
                context = self.return_weekly_questions_save_weight(weekly_weight, id_user)

            # return next advice
            if self.end is False:
                if advice_to_user == 1:

                    self.add_advices_to_user(id_user)
                context["advice"] = self.return_weekly_advice(id_user)

        return context

    def return_start_discussion(self, id_user, old_robot_question, data_weight_user, user_answer):
        """
        return robot question, user answer and robot answer,
        save user's advices and weight data
        """
        context = {}
        # get list_data (contains id robot
        # questions of the discussion space)
        list_data = self.new_questions_list.create_questions_id_list()

        # if the questionnaire has not yet started
        # FIRST ID QUESTION OF THE LIST_DATA
        actual_weight = data_weight_user.get("actual_weight")
        if old_robot_question is False and actual_weight is False:
            id_next_question = min(list_data)

        # if the questionnaire has yet started
        else:
            try:
                # SAVE ADVICES TO USER
                robot_question_id = RobotQuestion.objects.values_list("id")
                old_question_id = robot_question_id.get(text=old_robot_question)[0]
                user_answer_id = UserAnswer.objects.values_list("id").get(text=user_answer)
                self.save_advices_to_user(user_answer_id, old_question_id, id_user)

                # GET ID LAST QUESTION OF THE LIST_DATA
                index_old_id = list_data.index(old_question_id)

            # LAST QUESTION IS WEIGHT
            # GOAL QUESTION
            # > DEFINED GOAL WEIGHT
            except RobotQuestion.DoesNotExist:
                context = self.return_goal_weight_text_save_weight(data_weight_user, id_user)
                return context

            # get the robot answer
            robot_answer = DiscussionSpace.objects.values_list("robot_answer"). \
                filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
            context["robot_answer"] = robot_answer

            # if the user's answer causes the end of the discussion
            # id discussion space concerned : 2 and 3
            id_old_discussion = DiscussionSpace.objects.values_list("id"). \
                filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
            if id_old_discussion in (2, 3) or id_old_discussion in (2, 3):
                return context

            try:
                # GET ID OF THE NEXT QUESTION OF THE LIST_DATA
                id_next_question = list_data[index_old_id + 1]

            # if the questionnaire is finished
            # get goal weight questions
            except IndexError:
                context["goal_weight_text"] = self.goal_text
                context["dict_questions"] = self.dict_questions
                return context

        # get the robot question and the user's answers
        robot_question = RobotQuestion.objects.values_list("text").get(id=id_next_question)[0]
        context["question"] = robot_question
        answers_id = DiscussionSpace.objects.values_list("user_answer")\
            .filter(robot_question=id_next_question)
        if answers_id[0][0] is not None:
            answers_text_list = []
            for answer_id in answers_id:
                text = UserAnswer.objects.values_list("text")
                answers_text_list.append(text.get(id=answer_id[0])[0])
            context["answers"] = answers_text_list

        return context

    def return_goal_weight_text_save_weight(self, data_dict, id_user):
        """
        return the goal weight question
        and save the user's answers
        """
        # get robot advice to user : defined this weight goal
        actual_weight = data_dict.get("actual_weight")
        if actual_weight is not False:

            # if the user answered to the goal weight question
            # the parser method returned an error message
            # and add in the context the weight goal question
            context = self.parser_weight(data_dict)[1]
            if context:
                context["goal_weight_text"] = self.goal_text
                context["dict_questions"] = self.dict_questions
                return context

            # if the user's answer is validate
            data_validate = self.parser_weight(data_dict)[0]
            if data_validate is True:

                # get data
                goal = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[0]
                advice = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[1]
                final_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[2]

                # if user's goal weight is validate
                if goal != "impossible":
                    # create the end text
                    # of the questionnaire
                    id_type = RobotQuestionType.objects.values_list("id").get(type="end start")[0]
                    text = RobotQuestion.objects.values_list("text")
                    start_text_end = text.get(robot_question_type=id_type)[0]
                    text = advice + start_text_end

                    context = {}
                    try:
                        user = get_user_model()
                        user = user.objects.get(id=id_user)
                        ProfileUser.objects.values_list("starting_weight").get(user=user)[0]
                        text = "Ton premier objectif de poids a déjà " \
                               "été défini à - " + str(goal) + " kg."
                        context["robot_answer"] = text

                    # save user's data
                    except ProfileUser.DoesNotExist:
                        user = get_user_model()
                        user = user.objects.get(id=id_user)
                        ProfileUser.objects.create(user=user, starting_weight=actual_weight,
                                                   actual_goal_weight=goal,
                                                   final_weight=final_weight)
                        ResultsUser.objects.create(user=user, weight=actual_weight)
                        context["robot_answer"] = text

                    # means that the user have
                    # answered at all questions start
                    user = HistoryUser.objects.get(user=id_user)
                    user.start_questionnaire_completed = True
                    user.save()
                    self.end_questions_start = True

                # if user's goal weight is not validate
                else:
                    context["robot_answer"] = advice

            return context

    def save_advices_to_user(self, user_answer_id, old_question_id, id_user):
        """ save advices to user """
        # get data
        id_advice = DiscussionSpace.objects.values_list("robot_advices"). \
            filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]

        # if the user's answer
        # contains a robot advice
        if id_advice is not None:

            # get user's advices list
            user = self.user.objects.get(id=id_user)
            advices_user_id = user.advices_to_user.values_list("id")

            # get advices by question
            # in discussion space
            id_advices_question = DiscussionSpace.objects.values_list("robot_advices")\
                .filter(robot_question=old_question_id)

            # if the user has already given
            # another answer to this question :
            # delete the old advice
            for advices_question in id_advices_question:
                for advices_user in advices_user_id:
                    if advices_user[0] == advices_question[0]:
                        user.advices_to_user.remove(advices_user)

            # add a new advice to user
            advice = RobotAdvices.objects.get(id=id_advice)
            AdvicesToUser.objects.create(user=user, advice=advice)

    def return_weekly_advice(self, id_user):
        """
        return the next
        weekly advice
        """
        # get user
        user = self.user.objects.get(id=id_user)

        # if it's a new week
        if self.new_week is True:
            # delete last user's advice
            last_advice = user.advices_to_user.values_list("id").\
                order_by("robot_advice_type").first()
            user.advices_to_user.remove(last_advice)

        # get new user's advice
        text = user.advices_to_user.values_list("text")
        new_advices_user_text = text.order_by("robot_advice_type").first()[0]

        return new_advices_user_text

    def return_weekly_questions_save_weight(self, weekly_weight, id_user):
        """
        return weekly question
        and save user's answer
        """
        # get data
        context = {}
        weighing_date = ResultsUser.objects.values_list("weighing_date")
        last_weighing_date = weighing_date.filter(user=id_user).order_by("weighing_date").last()[0]
        one_week_after_weighing = last_weighing_date + timedelta(days=7)
        present = datetime.now()
        present_date = present.date()

        # one week after
        # the weighing last
        if present_date >= one_week_after_weighing:

            # if the user gave
            # his weekly weight
            if weekly_weight is not False:

                # if the user has reached
                # his weight goal
                final_weight = ProfileUser.objects.values_list("final_weight").get(user=id_user)[0]
                if float(weekly_weight) <= final_weight:
                    context["robot_comment"] = self.return_text_congratulations_restart_program\
                        (id_user)
                    self.end = True

                # save weight
                else:
                    context["robot_comment"] = "J'ai bien pris note de ton poids, " \
                                               "tu trouveras un récapitulatif dans " \
                                               "l'onglet résultats."
                    user = self.user.objects.get(id=id_user)
                    ResultsUser.objects.create(user=user, weight=weekly_weight)
                    self.new_week = True

            # create robot question
            else:
                context["robot_comment"] = "Bonjour ! J'éspère que ta semaine " \
                                           "s'est bien passée ? Que donne ta pesée " \
                                           "ce matin ?"
                context["robot_weekly_weight"] = True

        # during the first week after
        # the weighing last : create robot text
        else:
            month = calendar.month_name[one_week_after_weighing.month]
            date = "" + calendar.day_name[one_week_after_weighing.weekday()] + \
                   " " + str(one_week_after_weighing.day) \
                   + " " + month + ""
            context["robot_comment"] = "Retrouvons nous ici {} pour faire le point " \
                                       "sur tes prochains résultats et voir ton nouveau " \
                                       "challenge !".format(date)

        return context

    def add_advices_to_user(self, id_user):
        """
        add new robot
        advices to user
        """
        # get data
        advice_type_id = RobotAdviceType.objects.values_list("id").get(type="default")
        advices_id = RobotAdvices.objects.values_list("id").filter(robot_advice_type=advice_type_id)

        # add new advices to user
        for advice_id in advices_id:
            advice = RobotAdvices.objects.get(id=advice_id[0])
            user = self.user.objects.get(id=id_user)
            AdvicesToUser.objects.create(user=user, advice=advice)

    @classmethod
    def return_text_congratulations_restart_program(cls, id_user):
        """
        return congratulation text
        and restart program
        """
        # get data
        user = get_user_model()
        pseudo = user.objects.values_list("username").get(id=id_user)[0]

        # create congratulation text
        text = "Félicitation {} ! Tu as atteints ton objectif !".format(pseudo)

        # restart the program
        # and delete user's data
        user = HistoryUser.objects.get(user=id_user)
        user.start_questionnaire_completed = False
        user.save()
        ProfileUser.objects.filter(user=id_user).delete()
        ResultsUser.objects.filter(user=id_user).delete()
        AdvicesToUser.objects.filter(user=id_user).delete()

        return text

    @classmethod
    def parser_weight(cls, data_dict):
        """
        check if the user's
        answer is valid
        """
        # get user's answer
        context = {}
        actual_weight = data_dict.get("actual_weight")
        goal_weight = data_dict.get("weight_goal")

        # if not valid
        # create an error message
        if float(goal_weight) >= float(actual_weight):
            text = "Ton objectif doit être inférieur à ton poids actuel."
            context = {"error_message": text}
            validate = False

        # if valid
        else:
            validate = True

        return validate, context
