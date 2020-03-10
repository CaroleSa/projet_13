#! /usr/bin/env python3
# coding: UTF-8

""" Context processor """


# Imports
from django.conf import settings
from django.contrib.auth import get_user_model
from account.models import HistoryUser, IdentityUser


def start_questionnaire_completed_context(request):
    user = get_user_model()
    try:
        id = user.objects.get(id=request.user.id)
        start_questionnaire_completed = HistoryUser.objects.values_list("start_questionnaire_completed") \
            .get(user=id)[0]
        return {"start_questionnaire_completed": start_questionnaire_completed}
    except:
        return {"start_questionnaire_completed": False}
