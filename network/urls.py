from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/(?P<info>.*)$', views.login_page),
    url(r'^registration', views.registration_page)
]
