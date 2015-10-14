from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'utube.views.index'),
    url(r'^callback/$', 'utube.views.callback'),
    url(r'^videos/$', 'utube.views.videos'),
    url(r'^recommend/$', 'utube.views.recommend')
]
