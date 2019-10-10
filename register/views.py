from django.shortcuts import render
from .forms import RegisterForm
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("THIS IS THE REGISTRATION PAGE")



def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return HttpResponse("Successfully Registered!")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

