#! /usr/bin/env python3
# coding: UTF-8

""" User models """

# imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.timezone import now
from datetime import date


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class IdentityUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True,
                                validators=[UnicodeUsernameValidator()],
                                verbose_name='username')
    email = models.EmailField(max_length=254, unique=True, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]


class StatusUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. '
                                                          'A user will get all permissions granted '
                                                          'to each of their groups.',
                                    related_name='user_set',
                                    related_query_name='user',
                                    to='auth.Group',
                                    verbose_name='groups')
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                              related_name='user_set',
                                              related_query_name='user',
                                              to='auth.Permission',
                                              verbose_name='user permissions')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user '
                                                            'can log into this admin site.',
                                   verbose_name='staff status')
    is_superuser = models.BooleanField(default=False,
                                       help_text='Designates that this user has all permissions without '
                                                 'explicitly assigning them.',
                                       verbose_name='superuser status')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should '
                                                            'be treated as active. Unselect this instead '
                                                            'of deleting accounts.',
                                    verbose_name='active')


class HistoryUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=now, verbose_name='date joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')


class ProfileUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    starting_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    final_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)


class ResultsUser(models.Model):
    user = models.ForeignKey(IdentityUser, on_delete=models.CASCADE)
    weighing_date = models.DateField(default=date.today, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
