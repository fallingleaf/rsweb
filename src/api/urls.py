from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view()),
    url(r'^auth/signup/$', views.signup, name='rest_signup'),
    url(r'^auth/login/$', views.LoginView.as_view(), name='rest_login'),
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='rest_logout'),
    url(r'^contact', views.contact, name='rest_contact'),
    # url(r'^auth/fb/$', views.FacebookLogin.as_view(), name='fb_login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
