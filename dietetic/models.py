#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic models """

# imports
from django.db import models
from django.conf import settings


class RobotQuestionType(models.Model):
    type = models.CharField(max_length=20, unique=True)


class RobotAdviceType(models.Model):
    type = models.CharField(max_length=20, unique=True)


class RobotQuestion(models.Model):
    robot_question_type = models.ForeignKey(RobotQuestionType, on_delete=models.CASCADE)
    text = models.CharField(max_length=700, unique=True)


class RobotAdvices(models.Model):
    robot_advice_type = models.ForeignKey(RobotAdviceType, on_delete=models.CASCADE)
    advices_to_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    text = models.CharField(max_length=700, unique=True)


class UserAnswer(models.Model):
    discussion_space = models.ManyToManyField(RobotQuestion, through='RobotAnswer')
    text = models.CharField(max_length=200, null=True, unique=True)


class RobotAnswer(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    text = models.CharField(max_length=700, null=True)
