#! /usr/bin/env python3
# coding: UTF-8

""" Admin account app """

# imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from account.models import AdvicesToUser


user_model = get_user_model()


class UserCreationForm(ModelForm):
    class Meta:
        model = user_model
        fields = ["username", "email", "password", "is_staff", "is_superuser"]

    def save(self, commit=True):
        # Save the provided
        # password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(user_model)
class CustomUserAdmin(admin.ModelAdmin):
    """ CustomUserAdmin class """
    form = UserCreationForm
    list_display = ["username", "email", "last_login", "is_staff", "is_superuser"]
    list_filter = ["is_staff", "is_superuser"]


class AccountAdmin(admin.ModelAdmin):
    """ AccountAdmin class """
    list_display = ["user", "advice"]
    list_filter = ["user"]


admin.site.register(AdvicesToUser, AccountAdmin)
