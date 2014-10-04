from django.conf.urls import patterns, include, url
from django.contrib import admin

from bonfiremanager import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonfiremanager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
