from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

from user.token import TokenGenerator
from user.form import RegistrationForm, UserLoginForm

User = get_user_model()
acc_active_token = TokenGenerator()

def registration(request):
    if request.method != 'POST':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            try:
                exist_user = User.objects.get(email=email)
                if not exist_user.is_active:
                    exist_user.delete()
                else:
                    return render(request, 'register/register.html', {
                        'form': form,
                        'error': 'Пользователь с таким email уже существует'
                    })
            except User.DoesNotExist:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = acc_active_token.make_token(user)
            message = render_to_string('register/activate_email.html', {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
            })
            email_subject = 'Активация аккаунта'

            email_message = EmailMultiAlternatives(email_subject, message, to=[email])
            email_message.attach_alternative(message, "text/html")
            email_message.send()

            print("✅ Письмо отправлено на", email)

            return render(request, 'register/register_email_message.html', {'email': email})

    return render(request, 'register/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and acc_active_token.check_token(user, token):
        if (timezone.now() - user.date_joined).total_seconds() < 900:  # 15 минут
            user.is_active = True
            user.save()
            return render(request, 'register/success_activate.html')
    return render(request, 'register/fail_activate.html')

def userLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                auth_login(request, user)
                return redirect('main_page')
    else:
        form = UserLoginForm()
    return render(request, 'register/login.html', {'form': form})


def userLogout(request):
    logout(request)
    return redirect('main_page')
