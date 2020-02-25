from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'dietetic/index.html', context)

def dietetic_space(request):
    context = {}
    return render(request, 'dietetic/dietetic_space.html', context)

def my_results(request):
    context = {}
    return render(request, 'dietetic/my_results.html', context)