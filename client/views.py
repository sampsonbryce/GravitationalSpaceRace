from django.shortcuts import render
from django.template import loader


# Create your views here.
def index(request):
    # template = loader.get_template('client/index.html')
    return render(request, 'client/index.html', {})
