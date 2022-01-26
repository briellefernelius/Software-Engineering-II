from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'mysite/home.html')


def main(request):
    return render(request, 'mysite/main.html')
