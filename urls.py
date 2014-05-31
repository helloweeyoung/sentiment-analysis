from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^sa/', include('myproject.sa.urls')),
    (r'^chart/', include('myproject.charting.urls')),
    (r'^', include('myproject.feeds.urls')),
    # Profile application
    (r'^accounts/', include('myproject.userprofile.urls.en')),
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')), #django comments
)

#if settings.DEBUG:
urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$',
        'serve', {
        'document_root': '/home/weiyang/webapps/analytics/myproject/media',
        'show_indexes': True }),)
