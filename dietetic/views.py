from django.shortcuts import render


def index(request):
    return render(request, 'dietetic/index.html')

def dietetic_space(request):
    return render(request, 'dietetic/dietetic_space.html')

def my_results(request):
    return render(request, 'dietetic/my_results.html')