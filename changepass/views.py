from django.shortcuts import render
from OneApply.constants import UserType
from django.shortcuts import redirect
from .forms import changepassForm
from django.contrib.auth.hashers import make_password
from register.models import Student, Admin_Staff
from django.contrib.auth.hashers import check_password


def index(request):
    context = {
        "form": changepassForm(),
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    if not request.session.get("is_login", None):
        return redirect("landingpage:index")
    form = None
    if request.method == "POST":
        form = changepassForm(request.POST)
        match_error = False
        if form is not None and form.is_valid():
            newpassword = form.cleaned_data["new_password"]
            old_password = form.cleaned_data["old_password"]
            username = request.session.get("username", None)
            encrypt_pwd = make_password(newpassword)
            if request.session.get("user_type", None) == UserType.ADMIN_STAFF:
                p = Admin_Staff.objects.get(username=username)
                if check_password(old_password, p.password):
                    p.password = encrypt_pwd
                    p.save()
                else:
                    match_error = True
            elif request.session.get("user_type", None) == UserType.STUDENT:
                p = Student.objects.get(username=username)
                if check_password(old_password, p.password):
                    p.password = encrypt_pwd
                    p.save()
                else:
                    match_error = True
            if match_error == False:
                return redirect("landingpage:index")
            else:
                context = {"form": form, "match_error": match_error}
                return render(request, "changepass/index.html", context)
        else:
            context = {"form": form, "match_error": match_error}
            return render(request, "changepass/index.html", context)
        print
    return render(request, "changepass/index.html", context)


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")


# Create your views here.
