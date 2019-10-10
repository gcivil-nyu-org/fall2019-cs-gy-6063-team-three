from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm


def login_user(request):
    template_name = 'login/index.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            return HttpResponse("Okay")
    else:
        form = LoginForm()
    return render(request,template_name,{'form': form})


