from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def base(request):
    return render(request, "users/base.html")


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

