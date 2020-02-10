from django.shortcuts import render

# Create your views here.
def create_account(request):
    return render(request, 'account/create_account.html')