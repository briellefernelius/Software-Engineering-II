
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.


def account(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'payment/account.html', {'form': form})
