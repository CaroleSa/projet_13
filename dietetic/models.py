#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic models """

# imports
from django.db import models


class RobotQuestionType(models.Model):
    """ RobotQuestionType model """
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Type de question"


class RobotAdviceType(models.Model):
    """ RobotAdviceType model """
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Type de conseil"

class RobotQuestion(models.Model):
    """ RobotQuestion model """
    robot_question_type = models.ForeignKey(RobotQuestionType, on_delete=models.CASCADE)
    text = models.CharField(max_length=700, unique=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Question"


class RobotAdvices(models.Model):
    """ RobotAdvices model """
    robot_advice_type = models.ForeignKey(RobotAdviceType, on_delete=models.CASCADE)
    text = models.CharField(max_length=1700, unique=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Conseil"


class UserAnswer(models.Model):
    """ UserAnswer model """
    discussion_space = models.ManyToManyField(RobotQuestion, through='DiscussionSpace')
    text = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Réponse"


class DiscussionSpace(models.Model):
    """ DiscussionSpace model """
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, null=True)
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE, null=True)
    robot_answer = models.CharField(max_length=700, null=True)

    class Meta:
        unique_together = (("user_answer", "robot_question"),)

    def __str__(self):
        return self.robot_answer

    class Meta:
        verbose_name = "Echange"
