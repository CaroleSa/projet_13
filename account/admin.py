#! /usr/bin/env python3
# coding: UTF-8

""" Admin account app """

# imports
from django.contrib import admin
from account.models import IdentityUser


@admin.register(IdentityUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
