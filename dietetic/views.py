from django.shortcuts import render
from django.contrib.auth import get_user_model, logout


def index(request):
    context = {}
    user = get_user_model()

    # USER'S DEACTIVATION AND DISPLAY THE INDEX PAGE
    # if the user clicks on the logo "supprimer mon compte"
    delete_account = request.POST.get('delete_account', 'False')
    if delete_account == 'True':
        user_account = user.objects.get(email=request.user.email)
        logout(request)
        user_account.is_active = False
        user_account.save()
        print(user_account.is_active, user_account.email, "quand compte supprimé")
        context = {'error_message': "Votre compte a bien été supprimé."}

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
