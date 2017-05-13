from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, force_bytes, force_text
from django import forms
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.core.validators import RegexValidator
import socket
import os


class UserRegistrationForm(UserCreationForm):
    """A user registration form for user creation.

    Inherits from UserCreationForm.
    """

    first_name = forms.CharField(required=True, min_length=2)
    last_name = forms.CharField(required=True, min_length=2)
    username = forms.CharField(required=True,
                               min_length=6, validators=[
                                   RegexValidator(
                                       regex='^[a-zA-Z0-9]*$',
                                       message='Username must be Alphanumeric!',
                                       code='invalid_username'
                                   ),
                               ])
    email = forms.CharField(required=True, widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop('host', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()
            self.email_token(user)
        return user

    def email_token(self, user):
        """Generate activation email and to user else write to file."""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        subject = 'Account Activation - Enstitute'
        text_content = 'You have registered for an account with Enstitute.'
        activation_link = 'http://{0}/accounts/user/validate/{1}/{2}'.format(
            self.host, force_text(uid), token)
        html_content = '<p>Click --><a href="%s" rel="nofollow">here</a><-- to activate your account.</p>' % activation_link
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        to_email = user.email
        message = EmailMultiAlternatives(
            subject, text_content, from_email, [to_email])
        message.attach_alternative(html_content, 'text/html')
        try:
            message.send()
        except socket.error as socket_err:
            filename = user.username + '_activation_fail'
            with open(os.path.join(os.getcwd(), filename), 'w+') as fn:
                fn.write('email: \t\t\t\t' + str(user.email) + '\nactivation link: \t' +
                         str(activation_link) + '\nerror: \t\t\t\t' + str(socket_err))
                fn.close()


class UserLoginForm(AuthenticationForm):
    """A user registration form for user creation.

    Inherits from AuthenticationForm.
    """

    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
