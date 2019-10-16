from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import RegisterForm


def register_user(request, user_type):
    if user_type == "Student":
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['input_password']
                f = form.save(commit=False)
                f.password = password
                f.save()
                return HttpResponse("Registered Successfully!")
        else:
            form = RegisterForm()       
    return render(request, "register/index.html", {'form': form})
