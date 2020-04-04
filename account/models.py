#! /usr/bin/env python3
# coding: UTF-8

""" User models """

# imports
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.timezone import now
from dietetic.models import RobotAdvices
# pylint: disable=no-member


class UserManager(BaseUserManager):
    """ UserManager class """
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user
        with the given username,
        email, and password
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
        Creates and saves a superuser
        with the given email and password
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
    """ IdentityUser model """
    username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()],
                                verbose_name='pseudo')
    email = models.EmailField(max_length=254, unique=True, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='mot de passe')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='dernière connexion')
    advices_to_user = models.ManyToManyField(RobotAdvices, through="AdvicesToUser")
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user '
                                                            'can log into this admin site.',
                                   verbose_name='statut staff')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has '
                                                                'all permissions without '
                                                                'explicitly assigning them.',
                                       verbose_name='statut super-utilisateur')
    user_permissions = models.ManyToManyField(blank=True,
                                              help_text='Specific permissions for this user.',
                                              related_name='user_set', related_query_name='user',
                                              to='auth.Permission',
                                              verbose_name='permissions utilisateur')
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. '
                                                          'A user will get all permissions granted '
                                                          'to each of their groups.',
                                    related_name='user_set', related_query_name='user',
                                    to='auth.Group', verbose_name='groupes')

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        """ Meta class """
        verbose_name = "Identité utilisateur"


class AdvicesToUser(models.Model):
    """ AdvicesToUser model """
    user = models.ForeignKey(IdentityUser, on_delete=models.CASCADE,
                             verbose_name='utilisateur')
    advice = models.ForeignKey(RobotAdvices, on_delete=models.CASCADE,
                               verbose_name='conseil')

    class Meta:
        """ Meta class """
        verbose_name = "A destination de l'utilisateur : conseil"


class StatusUser(models.Model):
    """ StatusUser model """
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE,
                                verbose_name='utilisateur')
    is_active = models.BooleanField(default=True,
                                    help_text='Designates whether this '
                                              'user should be treated as '
                                              'active. Unselect this instead '
                                              'of deleting accounts.',
                                    verbose_name='est actif')

    class Meta:
        """ Meta class """
        verbose_name = "Statut utilisateur"


class HistoryUser(models.Model):
    """ HistoryUser model """
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE, verbose_name='utilisateur')
    date_joined = models.DateTimeField(default=now, verbose_name='date de création')
    start_questionnaire_completed = models.BooleanField(default=False,
                                                        verbose_name='questionnaire validé')

    def __str__(self):
        return self.date_joined

    class Meta:
        """ Meta class """
        verbose_name = "Historique utilisateur"


class ProfileUser(models.Model):
    """ ProfileUser model """
    user = models.OneToOneField(IdentityUser, on_delete=models.CASCADE, verbose_name='utilisateur')
    starting_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True,
                                          verbose_name='poids de démarrage')
    actual_goal_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True,
                                             verbose_name="poids total à perdre")
    final_weight = models.DecimalField(max_digits=4, decimal_places=1, null=True,
                                       verbose_name="poids d'objectif")

    def __str__(self):
        return self.starting_weight, self.final_weight

    class Meta:
        """ Meta class """
        verbose_name = "Profil utilisateur"


class ResultsUser(models.Model):
    """ ResultsUser model """
    user = models.ForeignKey(IdentityUser, on_delete=models.CASCADE, verbose_name='utilisateur')
    weighing_date = models.DateField(default=date.today, null=True, verbose_name='date de pesée')
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, verbose_name='poids')

    def __str__(self):
        return self.weighing_date, self.weight

    class Meta:
        """ Meta class """
        unique_together = (("user", "weighing_date"),)
        verbose_name = "Résultats utilisateur"
