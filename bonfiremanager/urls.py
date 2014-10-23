from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from bonfiremanager import api

from bonfiremanager import views

admin.autodiscover()

api_v1 = Api(api_name="v1")
api_v1.register(api.EventResource())
api_v1.register(api.TimeSlotResource())
api_v1.register(api.RoomResource())
api_v1.register(api.TalkResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonfiremanager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/', include(api_v1.urls)),
    url(r'^(?P<event_slug>[a-zA-Z0-9_-]+)$', views.EventView.as_view(), name='event-index'),
    url(r'^(?P<event_slug>[a-zA-Z0-9_-]+)/add$', views.AddTalkView.as_view(), name='talk-add'),
    url(r'^(?P<event_slug>[a-zA-Z0-9_-]+)/talk/(?P<talk_slug>[a-zA-Z0-9_-]+)$', views.TalkView.as_view(), name='talk'),
    url(r'^(?P<event_slug>[a-zA-Z0-9_-]+)/room/(?P<room_slug>[ a-zA-Z0-9_-]+)$', views.RoomView.as_view(), name='room'),
    url(r'^admin/', include(admin.site.urls)),
)
