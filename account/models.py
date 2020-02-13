#! /usr/bin/env python3
# coding: UTF-8

""" User models """

# imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
"""from datetime.date import today"""

"""class StatusUser(AbstractBaseUser):
    groups =
    user_permissions =
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def is_staff(self):
        return self.is_staff

    @property
    def is_superuser(self):
        return self.is_superuser

    @property
    def is_active(self):
        return self.is_active

class HistoryUser(AbstractBaseUser):
    date_joined =
    last_login ="""

"""class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)
    final_weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)

class ResultsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weighing_date = models.DateField(default=today, blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True)

class IdentityUser(AbstractBaseUser):
    username =
    email =
    password ="""

