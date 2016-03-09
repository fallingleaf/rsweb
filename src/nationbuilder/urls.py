from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from nationbuilder import views

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^events/clear$', views.event_clear, name="event-clear"),
    url(r'^events/summary$', views.event_summary, name="event-summary"),
    url(r'^events$', views.event_list, name="events"), 
    url(r'^', include(router.urls)), 
]

urlpatterns = format_suffix_patterns(urlpatterns)
