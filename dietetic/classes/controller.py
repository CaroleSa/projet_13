#! /usr/bin/env python3
# coding: UTF-8

""" Controller class """

# Imports
from django.contrib.auth import get_user_model
from dietetic.models import RobotAdvices, DiscussionSpace, RobotQuestion, RobotQuestionType, UserAnswer
from account.models import HistoryUser, ProfileUser, ResultsUser, IdentityUser
from dietetic.classes.questions_list import QuestionsList
from dietetic.classes.weight_advice_goal import WeightAdviceGoal


class Controller:

    def __init__(self):
        self.new_questions_list = QuestionsList()

    def controller_dietetic_space_view(self, id_user, old_robot_question, data_weight_user, user_answer):

        # if the user have not answered the start questions
        # create a list : robot questions start id
        start_questionnaire_completed = HistoryUser.objects.values_list("start_questionnaire_completed") \
            .get(user=id_user)
        if start_questionnaire_completed[0] is False:
            context = self.start_questions(id_user, old_robot_question, data_weight_user, user_answer)
            return context

    def start_questions(self, id_user, old_robot_question, data_weight_user, user_answer):
        context = {}
        print("questions non finies")
        list_data = self.new_questions_list.create_questions_id_list()

        # get and display robot question, user answer and robot answer
        actual_weight = data_weight_user.get("actual_weight")
        if old_robot_question is False and actual_weight is False:
            print("débute première question")
            id_next_question = min(list_data)
        else:
            print("fais les questions suivantes")
            try:
                old_question_id = RobotQuestion.objects.values_list("id").get(text=old_robot_question)[0]
                index_old_id = list_data.index(old_question_id)

            except RobotQuestion.DoesNotExist:
                # get user's answer : goal weight
                actual_weight = data_weight_user.get("actual_weight")
                if actual_weight is not False:
                    print("on parle poids")
                    new_weight_advice_goal = WeightAdviceGoal()
                    goal = new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[0]
                    advice = new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[1]
                    final_weight = new_weight_advice_goal.return_weight_advices_goal(data_weight_user)[2]

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
                            text = "Votre premier objectif de poids a déjà été défini à - " + str(goal) + " kg."
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

                    else:
                        context["robot_answer"] = advice
                    return context

            # get the robot answer
            user_answer_id = UserAnswer.objects.values_list("id").get(text=user_answer)
            robot_answer = DiscussionSpace.objects.values_list("robot_answer"). \
                filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
            context["robot_answer"] = robot_answer

            # if the user's answer causes the end of the discussion
            # id discussion space concerned : 2 and 3
            id_old_discussion = DiscussionSpace.objects.values_list("id"). \
                filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
            if id_old_discussion == 2 or id_old_discussion == 3:
                print("arret des questions suite à certaines questions")
                return context

            # get id of the next question
            try:
                id_next_question = list_data[index_old_id + 1]
                print("il existe encore des questions")
            # if there are no more questions
            except IndexError:
                print("il n'existe plus de questions, passons au poids")
                dict_questions = {"height": "Nous allons maintenant définir ton objectif. Quelle taille fais-tu ?",
                                  "actual_weight": "Quel est ton poids actuel ?",
                                  "cruising_weight": "Quel est ton poids de croisière (poids le plus longtemps "
                                                     "maintenu sans effort) ?",
                                  "weight_goal": "Quel est ton poids d'objectif ?"}
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

        # si questions finies ... mettre true à la valeur question de démarrage faite
        # sinon
        #       si utilisateur vient sur le site moins d'une semaine apres ses resultats :
        #       affiche texte doit attentdre telle date pour venir
        #       sinon :
        #           affiche texte question poids de la semaine
        #           si utilisateur a encore des challenges
        #               afficher nouveau challenge
        #           sinon (s'il n'a plus de challenges)
        #               affiche questionnaire pour recharger nouveau challenge
        #               si toujours pas de challenges:
        #               recharger avec challenges au pif ou defaults

        # récupère la réponse pour stocker le conseil correspondant
        # si conseil deja ajouté, ne pas le dupliquer et ne pas afficher d'erreur

        # si c'est sa première inscription sinon texte différent pour nouvel objectif

        return context