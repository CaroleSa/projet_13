from django.shortcuts import render


# Create your views here.
def create_account(request):
    context = {"create_account": "True"}
    return render(request, "dietetic/index.html", context)
