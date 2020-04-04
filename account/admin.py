#! /usr/bin/env python3
# coding: UTF-8

""" Admin account app """

# imports
from django.contrib import admin
from account.models import IdentityUser, AdvicesToUser


@admin.register(IdentityUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ["user", "advice"]


admin.site.register(AdvicesToUser, ProductAdmin)
