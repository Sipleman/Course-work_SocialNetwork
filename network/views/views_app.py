from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from network.views.utils.DB import DB

db = DB()


@login_required
def user_page(request, usr_id=""):
    print usr_id
    path = "/socnet/userpage/"
    user_info = {"authorized": True}

    if request.method == "POST":
        pass
    else:
        if usr_id != "":
            request_page_info = db.get_user_by_id(usr_id)
            if request_page_info["name"]:
                path += usr_id
                user_info.update(request_page_info.copy())
            else:
                return render(request, "Error-Page.html", {"user_info": user_info, "msg": "User doesn't exist"})

    return render(request, "User-Page.html", {"user_info": user_info, "user_page": path})


@login_required
def error_page(request):
    msg = "Something bad was wrong"
    user_info = {"authorized": True}
    if request.method == "GET":
        return render(request, "Error-Page.html", {"user_info": user_info, "msg": msg})


def mail_page(request):
    user = request.user
    if user.is_authenticated():
        db.get_user_mail()
