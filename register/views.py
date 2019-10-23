from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import RegisterForm
from .tokens import account_activation_token
from register.models import Student


def register_user(request, user_type):
    if user_type == "Student":
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['input_password']
                f = form.save(commit=False)
                f.is_active = False
                f.password = password
                f.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('register/activate_email.html', {'user': f,
                                                                   'domain':current_site.domain,
                                                                   'uid':urlsafe_base64_encode(force_bytes(f.pk)),
                                                                   'token':account_activation_token.make_token(f)})
                to_email = form.cleaned_data['email_address']
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse("Please confirm your email address to complete registration!")
        else:
            form = RegisterForm()       
    return render(request, "register/index.html", {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        f = Student.objects.get(id=uid)

    except(TypeError, ValueError, OverflowError, f.DoesNotExist):
        f = None
    if f is not None and account_activation_token.check_token(f, token):
        f.is_active = True
        f.save()
        return HttpResponse('Thank you for confirming your email. You can now login.')
    else:
        return HttpResponse('invalid token')
