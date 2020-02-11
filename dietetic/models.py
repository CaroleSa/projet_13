from django.db import models

class RobotQuestion(models.Model):
    text = models.CharField(unique=True)

class RobotQuestionType(models.Model):
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    type = models.CharField(unique=True)

class UserAnswer(models.Model):
    robot_questions = models.ManyToManyField(RobotQuestion, through='RobotAnswer')
    text = models.CharField()

class RobotAnswer(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)
    robot_question = models.ForeignKey(RobotQuestion, on_delete=models.CASCADE)
    text = models.CharField()

class RobotAdvices(models.Model):
    text = models.CharField()

class RobotAdviceType(models.Model):
    robot_advices = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE)
    type = models.CharField()

# clef etrangère entre robot_advices et table intermédiaire


