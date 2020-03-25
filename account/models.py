#! /usr/bin/env python3
# coding: UTF-8

""" User models """

# imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.timezone import now
from datetime import date
from dietetic.models import RobotAdvices


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        HistoryUser.objects.create(user=user)
        StatusUser.objects.create(user=user)

        return user


class IdentityUser(AbstractBaseUser):
    username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()],
                                verbose_name='username')
    email = models.EmailField(max_length=254, unique=True, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    advices_to_user = models.ManyToManyField(RobotAdvices)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user '
                                                            'can log into this admin site.',
                                   verbose_name='staff status')
    is_superuser = models.BooleanField(default=False,
                                       help_text='Designates that this user has all permissions without '
                                                 'explicitly assigning them.',
                                       verbose_name='superuser status')
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                              related_name='user_set',
                                              related_query_name='user',
                                              to='auth.Permission',
                                              verbose_name='user permissions')

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


class StatusUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. '
                                                          'A user will get all permissions granted '
                                                          'to each of their groups.',
                                    related_name='user_set',
                                    related_query_name='user',
                                    to='auth.Group',
                                    verbose_name='groups')

    is_active = models.BooleanField(default=True, help_text='Designates whether this user should '
                                                            'be treated as active. Unselect this instead '
                                                            'of deleting accounts.',
                                    verbose_name='active')


class HistoryUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=now, verbose_name='date joined')
    start_questionnaire_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.date_joined


class ProfileUser(models.Model):
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE)
    starting_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    actual_goal_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    final_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    def __str__(self):
        return self.starting_weight, self.final_weight


class ResultsUser(models.Model):
    user = models.ForeignKey(IdentityUser, on_delete=models.CASCADE)
    weighing_date = models.DateField(default=date.today, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    def __str__(self):
        return self.weighing_date, self.weight

    class Meta:
        unique_together = (("user", "weighing_date"),)
