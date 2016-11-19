from django.contrib.auth import authenticate
from django.contrib.auth.models import User


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

