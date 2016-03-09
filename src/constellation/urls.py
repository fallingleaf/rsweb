from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from jupiter.views import SignUpView

urlpatterns = [
    url(r'^$', 'jupiter.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    # api routing
    url(r'^api/', include('api.urls')),
    # nation builder routing
    url(r'^nationbuilder/', include('nationbuilder.urls')),
    # utube routing
    #url(r'^utube/', include('utube.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'jupiter.views.handler403'
handler404 = 'jupiter.views.handler404'
handler500 = 'jupiter.views.handler500'
