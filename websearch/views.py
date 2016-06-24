from django.shortcuts import render, render_to_response

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http.response import HttpResponse


def home(request):
    return render_to_response('home.html')


def indexation(request):
    return render_to_response('indexation.html')
