from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from network import forms


def check_login_date(login_form):
    username = login_form["login_name"].value()
    password = login_form["password"].value()
    user = authenticate(username=username, password=password)
    if user is not None:
        return user
    else:
        return None


def register_user(registration_form):
    username = registration_form["login_name"].value()
    password = registration_form["password"].value()
    email = registration_form["email"].value()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user is not None:
        return False
    else:
        user = User.objects.create_user(username, email, password)
        user.save()
        return True


def main_page(request, msg=""):
    authorized = False
    if request.user.is_authenticated():
        authorized = True
    return render(request, "Main-page.html", {"authorized": authorized, "msg": msg})


def login_page(request, info=""):
    if info == "":
        msg = "Enter your authenticate data"
    else:
        msg = "You are successfully registered!"

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        user = check_login_date(login_form)
        if user:
            login(request, user)
            msg = "Logged in"
        else:
            if not user:
                msg = 'Wrong data'

        return HttpResponseRedirect(reverse('Home', kwargs={'msg': msg}))
        return render(request, "login.html", {"login_form": login_form, "msg": msg})
    else:
        login_form = forms.LoginForm()

    return render(request, "login.html", {"login_form": login_form, "msg": msg})


def registration_page(request):
    msg = ""
    if request.method == "POST":
        registration_form = forms.RegistrationForm(request.POST)
        if registration_form.is_valid():
            if register_user(registration_form):
                return HttpResponseRedirect("login/info=registr_success")
            else:
                return render(request, "Registration-Page.html",
                              {"registration_form": registration_form, "msg": msg})
    else:
        registration_form = forms.RegistrationForm()

    return render(request, "Registration-Page.html", {"registration_form": registration_form})


def logout_page(request):
    msg = ""
    if request.user.is_authenticated():
        logout(request)
        msg = "Logged out"
        return HttpResponseRedirect(reverse('Home', kwargs={'msg': msg}))
