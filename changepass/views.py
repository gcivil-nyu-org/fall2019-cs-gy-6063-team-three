from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from OneApply.constants import UserType
from django.shortcuts import redirect
from .forms import changepassForm, resetPassFormStudent, resetPassFormAdmin
from django.contrib.auth.hashers import make_password
from register.models import Student, Admin_Staff
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

ALLOWED_CHARS = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789@#$%^&+=_-"


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
            if match_error is False:
                return redirect("landingpage:index")
            else:
                context = {"form": form, "match_error": match_error}
                return render(request, "changepass/index.html", context)
        else:
            context = {"form": form, "match_error": match_error}
            return render(request, "changepass/index.html", context)
    return render(request, "changepass/index.html", context)


def logout(request):
    request.session.flush()
    return redirect("landingpage:index")


def reset_password(request, user_type):
    if request.method == "POST":
        if user_type == UserType.STUDENT:
            form = resetPassFormStudent(request.POST)
            if form is not None and form.is_valid():
                email_address = form.cleaned_data["email_address"]
                password = User.objects.make_random_password(
                    allowed_chars=ALLOWED_CHARS
                )
                encrypt_pwd = make_password(password)
                p = Student.objects.get(email_address=email_address)
                p.password = encrypt_pwd
                p.save()
                current_site = get_current_site(request)
                mail_subject = "Password Reset"
                message = render_to_string(
                    "changepass/reset_pass_email.html",
                    {
                        "user": p,
                        "user_type": UserType.STUDENT,
                        "constant_ut_student": UserType.STUDENT,
                        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                        "password": password,
                        "domain": current_site.domain,
                    },
                )
                email = EmailMessage(mail_subject, message, to=[email_address])
                email.send()
                context = {
                    "user_type": UserType.STUDENT,
                    "constant_ut_student": UserType.STUDENT,
                    "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                }
                return render(request, "changepass/after_reset.html", context)
        elif user_type == UserType.ADMIN_STAFF:
            form = resetPassFormAdmin(request.POST)
            if form is not None and form.is_valid():
                email_address = form.cleaned_data["email_address"]
                password = User.objects.make_random_password(
                    allowed_chars=ALLOWED_CHARS
                )
                encrypt_pwd = make_password(password)
                p = Admin_Staff.objects.get(email_address=email_address)
                p.password = encrypt_pwd
                p.save()
                current_site = get_current_site(request)
                mail_subject = "Password Reset"
                message = render_to_string(
                    "changepass/reset_pass_email.html",
                    {
                        "user": p,
                        "user_type": UserType.ADMIN_STAFF,
                        "constant_ut_student": UserType.STUDENT,
                        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                        "password": password,
                        "domain": current_site.domain,
                    },
                )
                email = EmailMessage(mail_subject, message, to=[email_address])
                email.send()
                context = {
                    "user_type": UserType.ADMIN_STAFF,
                    "constant_ut_student": UserType.STUDENT,
                    "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                }
                return render(request, "changepass/after_reset.html", context)
    else:
        if user_type == UserType.STUDENT:
            form = resetPassFormStudent()
        elif user_type == UserType.ADMIN_STAFF:
            form = resetPassFormAdmin()
    context = {
        "form": form,
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "changepass/resetPass.html", context)
