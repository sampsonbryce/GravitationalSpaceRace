from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html', {})

def presentation(request):
    return render(request, 'core/presentation.html', {})




