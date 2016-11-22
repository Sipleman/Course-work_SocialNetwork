from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from network.views.utils.DB import DB

db = DB()


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
    registration_info = {"name": registration_form["name"].value(),
                         "lastname": registration_form["lastname"].value()}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user is not None:
        return False
    else:
        user = User.objects.create_user(username, email, password)
        print user.id
        registration_info["user_id"] = str(user.id)
        if db.insert_new_user(registration_info):
            user.save()
            return True
        else:
            return False

