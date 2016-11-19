from django.conf.urls import url

from network.views import views_auth
from network.views import views_app

urlpatterns = [

    # Main page
    url(r'^home/(?P<msg>.*)$', views_auth.main_page, name="Home"),
    # Auth urls
    url(r'^login/(?P<info>.*)$', views_auth.login_page, name="Login"),
    url(r'^logout', views_auth.logout_page, name="Logout"),
    url(r'^registration', views_auth.registration_page),

    # App urls
    url(r'^/(?P<id>[0-9])$', views_app.user_page, name="UserPage")

]
