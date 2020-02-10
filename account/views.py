from django.shortcuts import render
from django import template



# Create your views here.
def create_account(request):
    context = {"create_account": "True"}
    return render(request, "dietetic/index.html", context)

def login(request):
    return render(request, "dietetic/index.html")

def my_account(request):
    return render(request, "account/my_account.html")
