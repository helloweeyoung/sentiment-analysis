# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
urls.py
"""

from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

from views import rssfeed, atomfeed, mainview, opml, foaf, feed, userfeed, feed_callback

urlpatterns = patterns('',
    (r'^rss20.xml$', redirect_to,
      {'url':'/feed/rss/'}),
    (r'^feed/$', redirect_to,
      {'url':'/feed/atom/'}),
    (r'^feed/rss/$', rssfeed),
    (r'^feed/atom/$', atomfeed),

    (r'^feed/user/(?P<user>\d+)/tag/(?P<tag>.*)/$', redirect_to,
      {'url':'/feed/atom/user/%(user)s/tag/%(tag)s/'}),
    (r'^feed/user/(?P<user>\d+)/$', redirect_to,
      {'url':'/feed/atom/user/%(user)s/'}),
    (r'^feed/tag/(?P<tag>.*)/$', redirect_to,
      {'url':'/feed/atom/tag/%(tag)s/'}),

    (r'^feed/atom/user/(?P<user>\d+)/tag/(?P<tag>.*)/$', atomfeed),
    (r'^feed/atom/user/(?P<user>\d+)/$', atomfeed),
    (r'^feed/atom/tag/(?P<tag>.*)/$', atomfeed),
    (r'^feed/rss/user/(?P<user>\d+)/tag/(?P<tag>.*)/$', rssfeed),
    (r'^feed/rss/user/(?P<user>\d+)/$', rssfeed),
    (r'^feed/rss/tag/(?P<tag>.*)/$', rssfeed),

    (r'^user/(?P<user>\d+)/tag/(?P<tag>.*)/$', mainview),
    (r'^user/(?P<user>\d+)/$', mainview),
    (r'^tag/(?P<tag>.*)/$', mainview),

    (r'^opml/$', opml),
    (r'^foaf/$', foaf),

    (r'^accounts/profile/feeds/read/$', feed_callback),
    (r'^accounts/profile/feeds/(?P<url>\d+)/$', feed),
    (r'^accounts/profile/feeds/setting$', userfeed),
)
