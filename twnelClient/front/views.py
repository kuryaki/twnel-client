# Create your views here.

from django.shortcuts import render_to_response


def home(request):
    return render_to_response('index.html', {'result': ''})


def message(request):
    return render_to_response('index.html', {'result': 'sep'})
