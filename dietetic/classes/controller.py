#! /usr/bin/env python3
# coding: UTF-8

""" Controller class """

# Imports
from django.contrib.auth import get_user_model
from dietetic.models import RobotAdvices, DiscussionSpace, RobotQuestion, RobotQuestionType, UserAnswer
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.weight_advice_goal import WeightAdviceGoal
from django.db import connection


class Controller:

    def __init__(self):
        self.new_questions_list = QuestionsList()
        self.new_weight_advice_goal = WeightAdviceGoal()
        self.cursor = connection.cursor()

    def controller_dietetic_space_view(self, id_user, old_robot_question, data_weight_user, user_answer):

        # if the user have not answered the start questions
        # create a list : robot questions start id
        start_questionnaire_completed = HistoryUser.objects.values_list("start_questionnaire_completed") \
            .get(user=id_user)
        if start_questionnaire_completed[0] is False:
            context = self.return_start_discussion(id_user, old_robot_question, data_weight_user, user_answer)
            return context

        # SI L4UTILISATEUR A ATEINT SON POIDS D4OBJECTIF... final ou pas

        user = IdentityUser.objects.get(id=id_user)
        advice_to_user = user.advices_to_user.all()
        if start_questionnaire_completed[0] is True:
            if advice_to_user:
                self.return_advice_week_user(id_user)
                #return context
            """if not advice_to_user:
                # recharger en conseils
                return context
                self.return_questions_week_weight()"""

    def return_start_discussion(self, id_user, old_robot_question, data_weight_user, user_answer):
        """
        return robot question, user answer and robot answer,
        save user's advices and weight data
        """
        context = {}
        # get list_data (contains id robot questions of the discussion space)
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
                old_question_id = RobotQuestion.objects.values_list("id").get(text=old_robot_question)[0]
                user_answer_id = UserAnswer.objects.values_list("id").get(text=user_answer)
                self.save_advices_to_user(user_answer_id, old_question_id, id_user)

                # GET ID LAST QUESTION OF THE LIST_DATA
                index_old_id = list_data.index(old_question_id)

            # ID LAST QUESTION DON'T EXISTS > DEFINED GOAL WEIGHT
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
            if id_old_discussion == 2 or id_old_discussion == 3:
                return context

            try:
                # GET ID OF THE NEXT QUESTION OF THE LIST_DATA
                id_next_question = list_data[index_old_id + 1]

            # if the questionnaire is finished
            except IndexError:
                dict_questions = {"height": "Quelle taille fais-tu ?",
                                  "actual_weight": "Quel est ton poids actuel ?",
                                  "cruising_weight": "Quel est ton poids de croisière (poids le plus longtemps "
                                                     "maintenu sans effort) ?",
                                  "weight_goal": "Quel est ton poids d'objectif ?"}
                context["robot_answer"] = "Nous allons maintenant définir ton objectif."
                context["dict_questions"] = dict_questions
                return context

        # get the robot question and the user's answers
        robot_question = RobotQuestion.objects.values_list("text").get(id=id_next_question)[0]
        context["question"] = robot_question
        answers_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_question=id_next_question)
        if answers_id[0][0] is not None:
            answers_text_list = []
            for id in answers_id:
                answers_text_list.append(UserAnswer.objects.values_list("text").get(id=id[0])[0])
            context["answers"] = answers_text_list
        return context

    def return_goal_weight_text_save_weight(self, data_dict, id_user):

        # get robot advice to user : defined this weight goal
        context = {}
        actual_weight = data_dict.get("actual_weight")
        if actual_weight is not False:
            goal = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[0]
            advice = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[1]
            final_weight = self.new_weight_advice_goal.return_weight_advices_goal(data_dict)[2]

            # if user's goal weight is validate
            if goal != "impossible":
                # create goal weight text and end discussion text
                id_type = RobotQuestionType.objects.values_list("id").get(type="end start")[0]
                start_text_end = RobotQuestion.objects.values_list("text").get(robot_question_type=id_type)[0]
                text = advice + start_text_end

                # save user's data weight
                try:
                    user = get_user_model()
                    id = user.objects.get(id=id_user)
                    ProfileUser.objects.values_list("starting_weight").get(user=id)[0]
                    text = "Ton premier objectif de poids a déjà été défini à - " + str(goal) + " kg."
                    context["robot_answer"] = text

                except ProfileUser.DoesNotExist:
                    ProfileUser.objects.create(user=id, starting_weight=actual_weight,
                                               actual_goal_weight=goal, final_weight=final_weight)
                    ResultsUser.objects.create(user=id, weight=actual_weight)
                    context["robot_answer"] = text

                # means that the user have answered at all questions start
                user = HistoryUser.objects.get(user=id_user)
                user.start_questionnaire_completed = True
                user.save()

            # if user's goal weight is not validate
            else:
                context["robot_answer"] = advice

            return context

    def save_advices_to_user(self, user_answer_id, old_question_id, id_user):
        """ save advices to user """

        # if the user's answer contains a robot advice
        id_advice = DiscussionSpace.objects.values_list("robot_advices"). \
            filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
        if id_advice is not None:

            # get user's advices list
            user = IdentityUser.objects.get(id=id_user)
            advices_user_id = user.advices_to_user.values_list("id")

            # get advices by question in discussion space
            id_advices_question = DiscussionSpace.objects.values_list("robot_advices")\
                .filter(robot_question=old_question_id)

            # if the user has already given another answer to this question :
            # delete the old advice
            for advices_question in id_advices_question:
                for advices_user in advices_user_id:
                    if advices_user[0] == advices_question[0]:
                        user.advices_to_user.remove(advices_user)

            # add a new advice to user
            self.cursor.execute("INSERT INTO account_identityuser_advices_to_user (identityuser_id, robotadvices_id) "
                                "VALUES ({}, {})".format(id_user, id_advice))

    def return_advice_week_user(self, id_user):
        # on affiche en premanance le dernier challenge de la liste (trié par type)
        # get new user's advice
        user = IdentityUser.objects.get(id=id_user)
        new_advices_user_text = user.advices_to_user.values_list("text").order_by("robot_advice_type").first()[0]

        context = new_advices_user_text
        print(new_advices_user_text)

        return context
        # quand date de poids rentrée est égale à celle d'aujourd'hui
        # on supprime l'ancien challenge

