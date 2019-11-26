from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from OneApply.constants import UserType
from register.models import Student, Admin_Staff
from .forms import StudentRegisterForm, AdminStaffRegisterForm
from .tokens import account_activation_token


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
                    "register/activate_student_email.html",
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
                context = {
                    "user_type": UserType.STUDENT,
                    "constant_ut_student": UserType.STUDENT,
                    "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                }
                return render(request, "register/after_register.html", context)
        elif user_type == UserType.ADMIN_STAFF:
            form = AdminStaffRegisterForm(request.POST)
            if form is not None and form.is_valid():
                password = form.cleaned_data["input_password"]
                f = form.save(commit=False)
                f.password = password
                f.save()
                current_site = get_current_site(request)
                supervisor_mail_subject = "Verify your employee."
                supervisor_message = render_to_string(
                    "register/verify_employee.html",
                    {
                        "user": f,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(f.pk)),
                        "token": account_activation_token.make_token(f),
                    },
                )
                to_supervisor = form.cleaned_data["supervisor_email"]
                email = EmailMessage(
                    supervisor_mail_subject, supervisor_message, to=[to_supervisor]
                )
                email.send()
                staff_mail_subject = "Account and Employer Verification"
                staff_message = (
                    "An email has been sent to the supervisor contact you have provided. "  # noqa: E501
                    "Once they are able to verify your employment then you will receive a separate email "  # noqa: E501
                    "with instructions on activating your account."
                )
                to_staff = form.cleaned_data["email_address"]
                email2 = EmailMessage(staff_mail_subject, staff_message, to=[to_staff])
                email2.send()
                context = {
                    "user_type": UserType.ADMIN_STAFF,
                    "constant_ut_student": UserType.STUDENT,
                    "constant_ut_adminStaff": UserType.ADMIN_STAFF,
                }
                return render(request, "register/after_register.html", context)
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


def activate_student_account(request, uidb64, token):
    user = Student
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse("User Does Not Exist")
    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {
            "user_type": UserType.STUDENT,
            "constant_ut_student": UserType.STUDENT,
            "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        }
        return render(request, "register/after_verification_complete.html", context)
    else:
        return HttpResponse("Wrong Token")


def verify_employee_status(request, uidb64, token):
    user = Admin_Staff
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Admin_Staff.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse("User Does Not Exist")
    if account_activation_token.check_token(user, token):
        user.is_verified_employee = True
        user.save()
        current_site = get_current_site(request)
        mail_subject = "Activate your account"
        message = render_to_string(
            "register/activate_admission_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email_address
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return render(request, "register/after_verify.html")
    else:
        return HttpResponse("Wrong Token")


def activate_admission_account(request, uidb64, token):
    user = Admin_Staff
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Admin_Staff.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse("User Does Not Exist")
    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {
            "user_type": UserType.ADMIN_STAFF,
            "constant_ut_student": UserType.STUDENT,
            "constant_ut_adminStaff": UserType.ADMIN_STAFF,
        }
        return render(request, "register/after_verification_complete.html", context)
    else:
        return HttpResponse("Wrong Token")
