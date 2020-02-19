#! /usr/bin/env python3
# coding: UTF-8

""" User models """

# imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime.date import today


class StatusUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    groups =
    user_permissions =
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class HistoryUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login =


class ProfileUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    starting_weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)
    final_weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)


class ResultsUser(models.Model):
    user = models.ForeignKey(IdentityUser, on_delete=models.CASCADE)
    weighing_date = models.DateField(default=today, blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)


class IdentityUser(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    password =
