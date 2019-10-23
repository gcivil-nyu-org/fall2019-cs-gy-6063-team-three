from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from register.models import Student
from .forms import StudentRegisterForm, AdminStaffRegisterForm
from .tokens import account_activation_token
from OneApply.constants import UserType


def register_user(request, user_type):
    form = None
    if request.method == "POST":
        if user_type == UserType.STUDENT:
            form = StudentRegisterForm(request.POST)
            if form is not None and form.is_valid():
                password = form.cleaned_data["input_password"]
                f = form.save(commit=False)
                f.password = password
                f.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account."
                message = render_to_string(
                    "register/activate_email.html",
                    {
                        "user": f,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(f.pk)),
                        "token": account_activation_token.make_token(f),
                    },
                )
                to_email = form.cleaned_data["email_address"]
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse(
                    "Please confirm your email address to complete registration!"
                )
        elif user_type == UserType.ADMIN_STAFF:
            form = AdminStaffRegisterForm(request.POST)
            if form is not None and form.is_valid():
                password = form.cleaned_data["input_password"]
                f = form.save(commit=False)
                f.password = password
                f.save()
                return HttpResponse("Registered Successfully!")
    else:
        if user_type == UserType.STUDENT:
            form = StudentRegisterForm()
        elif user_type == UserType.ADMIN_STAFF:
            form = AdminStaffRegisterForm()
    context = {
        "form": form,
        "user_type": user_type,
        "constant_ut_student": UserType.STUDENT,
        "constant_ut_adminStaff": UserType.ADMIN_STAFF,
    }
    return render(request, "register/index.html", context)


def activate_user_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
        return HttpResponse("invalid token")
    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for confirming your email. You can now login.")
