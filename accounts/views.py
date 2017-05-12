from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
#from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, force_text
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import CustomUser

User = getattr(settings, 'AUTH_USER_MODEL')


def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home_page'))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, host=request.get_host())

        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            user = authenticate(
                username=username,
                password=form.cleaned_data.get('password1')
            )

            if user is None or not user.is_active:
                messages.error(request, 'Check email')
                return render(request, 'accounts/check_email.html')
            else:
                messages.error(
                    request, 'There was an error creating the user. Kindly email admin.')

        else:
            messages.error(request, 'Form error! Check listed errors.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register_user.html', {'form': form})


def login_user(request):
    next_page = request.GET.get('next').strip()
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home_page'))

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(
                username=username,
                password=form.cleaned_data.get('password')
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, 'Login successful. Welcome %s' % username)

                    if next_page:
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect(reverse('home_page'))
                else:
                    return render(request, 'accounts/check_email.html')

            else:
                messages.error(request, 'User does not exist.')

        else:
            messages.error(request, 'Form is invalid')

    else:
        form = UserLoginForm()
    return render(request, 'accounts/login_user.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return HttpResponseRedirect(reverse('home_page'))


def activate_user(request, uidb64, token):
    if uidb64 is not None and token is not None:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token) and not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Email verified! Proceed to login.')
            return HttpResponseRedirect(reverse('accounts:login_user'))

    messages.error(request, 'Invalid link.')
    return HttpResponseRedirect(reverse('home_page'))
