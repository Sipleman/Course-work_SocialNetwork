from django.shortcuts import render


def user_page(request):
    if request.method == "POST":
        pass
    else:
        pass
    return render(request, "User-Page.html")