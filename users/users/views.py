from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from requests import request
from .models import *
from django.db.models import Q
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import os
def search(request):
    return render(request, 'users/search.html')
def xyz(request):
    return render(request, 'users/xyz.html')


def home2(request):
    return render(request, 'users/home2.html')

def home(request):
    return render(request, 'users/home.html')
'''def login(request):
    return render(request, 'users/login.html')
'''

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='xyz')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
def ngo_list(request):
    ngos = NGO.objects.all()
    name_query = request.GET.get('name')
    location_query = request.GET.get('location')
    if name_query:
        ngos = ngos.filter(name__icontains=name_query)
    if location_query:
        ngos = ngos.filter(location__icontains=location_query)
    context = {
        'ngos': ngos,
        'name_query': name_query,
        'location_query': location_query,
    }
    return render(request, 'ngo_list.html', context)
'''from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
'''

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your homepage
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

"""def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html')
    def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home/')  # Change 'home' to the name of your home page URL pattern
        else:
            form = AuthenticationForm(request.POST)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})"""
def contactus(request):
    return render(request,"users/contactus.html",{})
def aboutus(request):
    return render(request,"users/About us.html",{})
def readmore(request):
    return render(request,"https://www.akshayapatra.org/donate-and-save-tax?utm_source=Search-Generic&utm_medium=Tax+Exemption-2023&utm_campaign=GDN-TAPF&gclid=Cj0KCQiAjbagBhD3ARIsANRrqEtqOp4YjzwzJ0sl6kkSehBFs8gYYMDNMiMGF59GCFifBygodLOxDbEaAu8BEALw_wcB")
