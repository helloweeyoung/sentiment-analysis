#-*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from views import text_input, text_analysis, text_history, feedback, test, opendocument, xhr_test

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^input$', text_input), 
    (r'^analysis$', text_analysis),
    (r'^history$', text_history),
    (r'^feedback$', feedback),
    (r'^test$', xhr_test),
    (r'^document/(?P<document>\d+)/$', opendocument),

    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

