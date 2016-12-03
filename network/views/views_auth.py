from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from views_app import db
# Create your views here.
from network import forms
from network.views.utils.auth_utils import check_login_date, register_user


def main_page(request, msg=""):
    user = request.user
    user_info = {}
    usrpath = "/socnet/userpage/"
    if user.is_authenticated():
        usrpath += str(user.id)
        user_info['authorized'] = True
        user_info['user_page'] = usrpath
        print usrpath
    else:
        if msg == "registered":
            msg = "Successfully registered"

    return render(request, "Main-page.html", {"user_info": user_info, "msg": msg})


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
            db.set_current_user(str(user.id))
            msg = "Logged in"
        else:
            if not user:
                msg = 'Wrong data'

        return HttpResponseRedirect(reverse('Home', kwargs={'msg': msg}))
        # return render(request, "login.html", {"login_form": login_form, "msg": msg})
    else:
        login_form = forms.LoginForm()

    return render(request, "login.html", {"login_form": login_form, "msg": msg})


def registration_page(request):
    msg = ""
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("home/")
    if request.method == "POST":
        registration_form = forms.RegistrationForm(request.POST)
        if registration_form.is_valid():
            if register_user(registration_form):
                return HttpResponseRedirect("/socnet/home/msg=registr_success")
            else:
                return render(request, "Registration-Page.html",
                              {"registration_form": registration_form, "msg": msg})
    else:
        registration_form = forms.RegistrationForm()

    return render(request, "Registration-Page.html", {"registration_form": registration_form})


@login_required
def logout_page(request):
    msg = ""
    if request.user.is_authenticated():
        logout(request)
        msg = "Logged out"
        return HttpResponseRedirect(reverse('Home', kwargs={'msg': msg}))
