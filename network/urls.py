from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/(?P<msg>.*)$', views.main_page, name="Home"),
    url(r'^login/(?P<info>.*)$', views.login_page, name="Login"),
    url(r'^logout', views.logout_page, name="Logout"),
    url(r'^registration', views.registration_page)
]
