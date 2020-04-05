#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic models """

# imports
from django.db import models


class RobotQuestionType(models.Model):
    """ RobotQuestionType model """
    type = models.CharField(max_length=20, unique=True,
                            verbose_name="type de question")

    def __str__(self):
        return self.type

    class Meta:
        """ Meta class """
        verbose_name = "Type de question"


class RobotAdviceType(models.Model):
    """ RobotAdviceType model """
    type = models.CharField(max_length=20, unique=True,
                            verbose_name="type de conseil")

    def __str__(self):
        return self.type

    class Meta:
        """ Meta class """
        verbose_name = "Type de conseil"


class RobotQuestion(models.Model):
    """ RobotQuestion model """
    robot_question_type = models.ForeignKey(RobotQuestionType,
                                            on_delete=models.CASCADE,
                                            verbose_name="type de question")
    text = models.CharField(max_length=700, unique=True,
                            verbose_name="question du robot")

    def __str__(self):
        return self.text

    class Meta:
        """ Meta class """
        verbose_name = "Question"


class RobotAdvices(models.Model):
    """ RobotAdvices model """
    robot_advice_type = models.ForeignKey(RobotAdviceType,
                                          on_delete=models.CASCADE,
                                          verbose_name="type de conseil")
    text = models.CharField(max_length=1700, unique=True,
                            verbose_name="conseil du robot")

    def __str__(self):
        return self.text

    class Meta:
        """ Meta class """
        verbose_name = "Conseil"


class UserAnswer(models.Model):
    """ UserAnswer model """
    discussion_space = models.ManyToManyField(RobotQuestion,
                                              through='DiscussionSpace')
    text = models.CharField(max_length=200, null=True, unique=True,
                            verbose_name="réponse de l'utilisateur")

    def __str__(self):
        return self.text

    class Meta:
        """ Meta class """
        verbose_name = "Réponse"


class DiscussionSpace(models.Model):
    """ DiscussionSpace model """
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE,
                                    null=True,
                                    verbose_name="réponse de l'utilisateur")
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE,
                                       verbose_name="question du robot")
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE,
                                      null=True,
                                      verbose_name="conseil du robot")
    robot_answer = models.CharField(max_length=700, null=True,
                                    verbose_name="réponse du robot")

    class Meta:
        """ Meta class """
        unique_together = (("user_answer", "robot_question"),)
        verbose_name = "Echange"
        ordering = ["id"]

    def __str__(self):
        return self.robot_answer
