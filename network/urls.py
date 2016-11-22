from django.conf.urls import url

from network.views import views_auth
from network.views import views_app



urlpatterns = [

    # Main page
    url(r'^home/(?P<msg>.*)$', views_auth.main_page, name="Home"),
    # url(r'$', views_auth.main_page, name="Home"),
    # Auth urls
    url(r'^login/(?P<info>.*)$', views_auth.login_page, name="Login"),
    url(r'^logout', views_auth.logout_page, name="Logout"),
    url(r'^registration', views_auth.registration_page),

    # App urls
    url(r'^userpage/(?P<usr_id>.[0-9])', views_app.user_page, name="UserPage"),
    url(r'^error/', views_app.error_page, name="UserPage"),
    url(r'^im/', views_app.mail_page, name="UserMail"),
    url(r'^send_msg/(?P<user_id>.[0-9])', views_app.send_msg, name="SendMessage"),
    url(r'^friend_request/', views_app.friend_request, name="FriendRequest")

]
