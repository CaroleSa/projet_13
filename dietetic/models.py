#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic models """

# imports
from django.db import models
from django.conf import settings


class RobotQuestion(models.Model):
    text = models.CharField(max_length=700, unique=True)


class RobotQuestionType(models.Model):
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, unique=True)


class UserAnswer(models.Model):
    discussion_space = models.ManyToManyField(RobotQuestion, through='RobotAnswer')
    text = models.CharField(max_length=200, null=True, unique=True)


class RobotAdvices(models.Model):
    advices_to_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    text = models.CharField(max_length=700, unique=True)


class RobotAnswer(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    text = models.CharField(max_length=700, null=True)


class RobotAdviceType(models.Model):
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, unique=True)
