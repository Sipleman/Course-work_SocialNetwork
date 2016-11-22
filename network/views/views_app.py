from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
        if usr_id != "" and request.user.id == usr_id:
            # This is page of user that requested page, content will be different
            request_page_info = db.get_user_by_id(usr_id)
            if request_page_info["name"]:
                path += usr_id
                user_info.update(request_page_info.copy())

            else:
                return render(request, "Error-Page.html", {"user_info": user_info, "msg": "User doesn't exist"})
        else:
            request_page_info = db.get_user_by_id(usr_id)
            if request_page_info["name"]:
                path += usr_id
                user_info.update(request_page_info.copy())
                user_info["id"] = usr_id
                print "adsasda"
            else:
                return render(request, "Error-Page.html", {"user_info": user_info, "msg": "User doesn't exist"})

    return render(request, "User-Page.html", {"user_info": user_info, "user_page": path})


@login_required
def error_page(request):
    msg = "Something bad was wrong"
    user_info = {"authorized": True}
    if request.method == "GET":
        return render(request, "Error-Page.html", {"user_info": user_info, "msg": msg})


@login_required
def mail_page(request):
    user = request.user
    if user.is_authenticated():
        msgs = db.get_user_mail(user.id)

        return render(request, "User-Msgs-Page.html", {"msgs": msgs})


@login_required
def send_msg(request, user_id=""):
    user = request.user
    if request.method == "POST":
        receiver = request.POST["receiver"]
        content = request.POST["content"]
        sender = user.id
        if db.send_message(receiver, content, sender):
            return HttpResponseRedirect("/socnet/im")
    else:
        receiver = user_id
        return render(request, "Send-Message-Page.html", {"receiver": receiver})


@login_required
def friend_request(request):
    pass