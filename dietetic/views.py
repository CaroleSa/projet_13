#! /usr/bin/env python3
# coding: UTF-8

""" views of the dietetic app """

# Imports
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
import datetime
from .models import RobotAdvices, DiscussionSpace, RobotQuestion, RobotQuestionType, UserAnswer
from account.models import HistoryUser
from .classes.questions_list import QuestionsList


def index(request):
    context = {}

    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')
    if logout_user == 'True':
        logout(request)

    # si l'utilisateur à comme conseil le manque de connaissance alimentaire,
    # affiche l'onglet programme

    return render(request, 'dietetic/index.html', context)


def dietetic_space(request):
    context = {}

    # if the user have not answered the first questions
    # create a list : robot questions start id
    start_questionnaire_completed = HistoryUser.objects.values_list("start_questionnaire_completed")\
        .get(user=request.user.id)
    if start_questionnaire_completed[0] is False:
        new_questions_list = QuestionsList()
        list_data = new_questions_list.create_questions_id_list()
        new_list = []
        for id in list_data:
            question = RobotQuestion.objects.get(id=id)
            type = question.robot_question_type.type
            if type == "start":
                new_list.append(id)
        list_data = new_list

    # get and display robot question, user answer and robot answer
    old_robot_question = request.POST.get('question', False)
    if old_robot_question is False:
        id_next_question = min(list_data)
    else:
        old_question_id = RobotQuestion.objects.values_list("id").get(text=old_robot_question)[0]
        index_old_id = list_data.index(old_question_id)

        # get the robot answer
        user_answer = request.POST.get('answer')
        user_answer_id = UserAnswer.objects.values_list("id").get(text=user_answer)
        robot_answer = DiscussionSpace.objects.values_list("robot_answer").\
            filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
        context["robot_answer"] = robot_answer

        # if the user's answer causes the end of the discussion
        # id discussion space concerned : 2 and 3
        id_old_discussion = DiscussionSpace.objects.values_list("id"). \
            filter(robot_question=old_question_id).get(user_answer=user_answer_id)[0]
        if id_old_discussion == 2 or id_old_discussion == 3 or id_old_discussion == 45:
            return render(request, 'dietetic/dietetic_space.html', context)

        # get id of the next question
        try:
            id_next_question = list_data[index_old_id + 1]

        # if there are no more questions
        except IndexError:

            list_robot_question = ["Nous allons maintenant définir ton objectif. Quelle taille fais-tu ?",
                                   "Quel est ton poids actuel ?",
                                   "Quel est ton poids de croisière (poids le plus longtemps maintenu sans effort) ?",
                                   "Quel est ton poids d'objectif ?"]
            # ici fonction poids
            user = HistoryUser.objects.get(user=request.user.id)
            user.start_questionnaire_completed = True
            user.save()
            return render(request, 'dietetic/dietetic_space.html', context)

    # get the robot question and the user's answers
    robot_question = RobotQuestion.objects.values_list("text").get(id=id_next_question)[0]
    context["question"] = robot_question

    answers_id = DiscussionSpace.objects.values_list("user_answer").filter(robot_question=id_next_question)
    print(answers_id[0])
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
    user_answer = request.POST.get('answer')


    # si c'est sa première inscription sinon texte différent pour nouvel objectif



    return render(request, 'dietetic/dietetic_space.html', context)


def my_results(request):
    context = {}

    starting_date = [2020, 5, 20]
    starting_weight = 60
    last_date = [2020, 7, 20]
    last_weight = 55
    starting_week = datetime.datetime(starting_date[0], starting_date[1], starting_date[2]).isocalendar()[1]
    last_week = datetime.datetime(last_date[0], last_date[1], last_date[2]).isocalendar()[1]
    number_week = last_week - starting_week
    lost_weight = starting_weight - last_weight
    average_weight_loss = round(lost_weight/number_week, 1)
    last_2_weighings = "ok"
    last_weighings = "ok"
    if average_weight_loss <= 0.3:
        text = "Petite moyenne de perte de poids"
    if average_weight_loss >= 0.4 <= 0.5:
        text = "Moyenne de perte de poids moyenne"
    if average_weight_loss >= 0.6 <= 0.8:
        text = "Bonne moyenne de perte de poids"
    if average_weight_loss >= 0.9:
        text = "Très bonne moyenne de perte de poids"

    if last_2_weighings == "ok":
        text = "Dernières pertes parfaites !"
    else:
        if last_weighings == "ok":
            text = "Dernières pertes moyennes !"
        else:
            text = "Dernières pertes mauvaises !"



    return render(request, 'dietetic/my_results.html', context)


def program(request):
    context = {}
    return render(request, 'dietetic/program.html', context)
