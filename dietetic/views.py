from django.shortcuts import render
from django.contrib.auth import get_user_model, logout


def index(request):
    context = {}
    # USER'S DISCONNECTION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the button "me déconnecter"
    logout_user = request.POST.get('logout', 'False')

    if logout_user == 'True':
        logout(request)

    return render(request, 'dietetic/index.html', context)


def dietetic_space(request):
    context = {}
    return render(request, 'dietetic/dietetic_space.html', context)


def my_results(request):
    context = {}
    return render(request, 'dietetic/my_results.html', context)
