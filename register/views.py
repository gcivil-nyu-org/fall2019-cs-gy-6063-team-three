from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import StudentRegisterForm, AdminStaffRegisterForm


def register_user(request, user_type):
    template_name = 'register/index.html'
    form = None
    if request.method == 'POST':
        if user_type == "student":
            form = StudentRegisterForm(request.POST)
        elif user_type == "admin_staff":
            form = AdminStaffRegisterForm(request.POST)
        if form is not None and form.is_valid():
            password = form.cleaned_data['input_password']
            f = form.save(commit=False)
            f.password = password
            f.save()
            return HttpResponse("Registered Successfully!")
    else:
        if user_type == "student":
            form = StudentRegisterForm()
        elif user_type == "admin_staff":
            form = AdminStaffRegisterForm()
    return render(request, template_name, {'form': form, 'user_type': user_type})

