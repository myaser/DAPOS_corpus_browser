# Create your views here.
from django.shortcuts import render


def main(request):
    return render(request, 'home.html', {'title': 'DAPOS'})


def search(request):
    return render(request, 'base.html')
