from django.shortcuts import render
from django import template
from .forms import Account



# Create your views here.
def create_account(request):
    context = {"create_account": "True"}
    return render(request, "dietetic/index.html", context)

def login(request):
    form = Account()
    context = {'form': form}
    return render(request, "dietetic/index.html", context)

def my_account(request):
    return render(request, "account/my_account.html")
