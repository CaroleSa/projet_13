#! /usr/bin/env python3
# coding: UTF-8

""" Dietetic models """

# imports
from django.db import models


class RobotQuestion(models.Model):
    text = models.CharField(unique=True)


class RobotQuestionType(models.Model):
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    type = models.CharField(unique=True)


class UserAnswer(models.Model):
    discussion_space = models.ManyToManyField(RobotQuestion, through='RobotAnswer')
    text = models.CharField()


class RobotAnswer(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    text = models.CharField()


class RobotAdvices(models.Model):
    advices_to_user = models.ManyToManyField(IdentityUser)
    text = models.CharField()


class RobotAdviceType(models.Model):
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    type = models.CharField()
