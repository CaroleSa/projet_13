from django.shortcuts import render
from django import template



# Create your views here.
def create_account(request):
    context = {"create_account": "True"}
    return render(request, "dietetic/index.html", context)

def login(request):
    context = {}
    return render(request, "dietetic/index.html", context)

def my_account(request):
    context = {}
    return render(request, "account/my_account.html", context)
