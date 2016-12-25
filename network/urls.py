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
    url(r'^userpage/wall/new_record', views_app.new_wall_record, name="NewWallRecord"),
    url(r'^userpage/wall/new_like', views_app.new_like, name="AddLike"),
    url(r'^userpage/wall/new_comment', views_app.new_comment, name="AddComment"),
    url(r'^userpage/wall/delete_post', views_app.delete_post, name="DeletePost"),

    url(r'^error/', views_app.error_page, name="UserPage"),
    url(r'^im/', views_app.mail_page, name="UserMail"),
    url(r'^send_msg/(?P<user_id>.[0-9])', views_app.send_msg, name="SendMessage"),
    url(r'^friend_request/', views_app.send_friend_request, name="FriendRequest"),
    url(r'^friends/', views_app.user_friends, name="Friends"),
    url(r'^delete_friend/', views_app.delete_friend, name="Delete Friend"),

    url(r'^sent/', views_app.user_sent_msgs, name="Sent msgs"),

    url(r'^requests/', views_app.user_requests, name="Friend requests"),

    url(r'^accept_request/', views_app.accept_request, name="Accept_request"),
    url(r'^decline_request/', views_app.decline_request, name="Decline_request")

]
