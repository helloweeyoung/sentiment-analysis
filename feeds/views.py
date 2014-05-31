# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
views.py
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.utils import feedgenerator
from django.shortcuts import render_to_response
from django.utils.cache import patch_vary_headers
from django.template import RequestContext, Context, loader

from models import Site
from fjlib import getcurrentsite, get_paginator, page_context, sitefeeds, get_extra_content
from fjcache import cache_set, cache_get


import urllib2

import feedparser

from form import *
from dataaccess import getuserfeeds, getsinglefeed, createdocument


from myproject.scrape.views import *

def initview(request):
    """ Retrieves the basic data needed by all feeds (host, feeds, etc)

    Returns a tuple of:
    1. A valid cached response or None
    2. The current site object
    3. The cache key
    4. The subscribers for the site (objects)
    5. The feeds for the site (ids)
    """

    site_id, cachekey = getcurrentsite(request.META['HTTP_HOST'], \
      request.META.get('REQUEST_URI', request.META.get('PATH_INFO', '/')), \
      request.META['QUERY_STRING'])
    response = cache_get(site_id, cachekey)
    if response:
        return response, None, cachekey, [], []

    site = Site.objects.get(pk=site_id)
    sfeeds_obj = sitefeeds(site)
    sfeeds_ids = [subscriber.feed.id for subscriber in sfeeds_obj]

    return None, site, cachekey, sfeeds_obj, sfeeds_ids

def blogroll(request, btype):
    """ View that handles the generation of blogrolls.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    # for some reason this isn't working:
    #
    #response = render_to_response('feedjack/%s.xml' % btype, \
    #  fjlib.get_extra_content(site, sfeeds_ids))
    #response.mimetype = 'text/xml; charset=utf-8'
    #
    # so we must use this:

    template = loader.get_template('feed/%s.xml' % btype)
    ctx = {}
    get_extra_content(site, sfeeds_ids, ctx)
    ctx = Context(ctx)
    response = HttpResponse(template.render(ctx) , \
      mimetype='text/xml; charset=utf-8')


    patch_vary_headers(response, ['Host'])
    cache_set(site, cachekey, response)
    return response

def foaf(request):
    """ View that handles the generation of the FOAF blogroll.
    """

    return blogroll(request, 'foaf')

def opml(request):
    """ View that handles the generation of the OPML blogroll.
    """

    return blogroll(request, 'opml')


def buildfeed(request, feedclass, tag=None, user=None):
    """ View that handles the feeds.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    object_list = get_paginator(site, sfeeds_ids, page=0, tag=tag, \
      user=user)[1]

    feed = feedclass(\
        title=site.title,
        link=site.url,
        description=site.description,
        feed_url='%s/%s' % (site.url, '/feed/rss/'))
    for post in object_list:
        feed.add_item( \
          title = '%s: %s' % (post.feed.name, post.title), \
          link = post.link, \
          description = post.content, \
          author_email = post.author_email, \
          author_name = post.author, \
          pubdate = post.date_modified, \
          unique_id = post.link, \
          categories = [tag.name for tag in post.tags.all()])
    response = HttpResponse(mimetype=feed.mime_type)

    # per host caching
    patch_vary_headers(response, ['Host'])

    feed.write(response, 'utf-8')
    if site.use_internal_cache:
        cache_set(site, cachekey, response)
    return response

def rssfeed(request, tag=None, user=None):
    """ Generates the RSS2 feed.
    """
    result = urllib2.Request('http://www.channelnewsasia.com/rss/latest_cna_sg_rss.xml')
    opener = urllib2.build_opener()
    f = opener.open(result)
    #return buildfeed('http://www.channelnewsasia.com/rss/latest_cna_sg_rss.xml', feedgenerator.Rss201rev2Feed, tag, user)
    return buildfeed(f, feedgenerator.Rss201rev2Feed, tag, user)


def atomfeed(request, tag=None, user=None):
    """ Generates the Atom 1.0 feed. 
    """
    return buildfeed(request, feedgenerator.Atom1Feed, tag, user)

def mainview(request, tag=None, user=None):
    """ View that handles all page requests.
    """

    response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
    if response:
        return response

    ctx = page_context(request, site, tag, user, (sfeeds_obj, \
      sfeeds_ids))

    response = render_to_response('feed/%s/post_list.html' % \
      (site.template), ctx)
    
    # per host caching, in case the cache middleware is enabled
    patch_vary_headers(response, ['Host'])

    if site.use_internal_cache:
        cache_set(site, cachekey, response)
    return response

#~


def feed_callback(request):
    #callback = request.GET.get('callback', '')
    #req = {}
    #req ['title'] = 'This is a constant result.'
    #response = json.ialize(req, ensure_ascii=False, stream=response)
    #response = callback + '();'
    #new_Transaction = document()
    url = request.POST.get('url', '')
    new_doc_id = createdocument(request.POST.get('title',''), request.user.username, url, getsource(url), request.POST.get('author',''), request.POST.get('summary',''))
    #new_Transaction.created_by = 'admin' #request.user.username #'admin'
    #new_Transaction.url = 'rur' #request.POST['url'] #'rur' #form.cleaned_data['url']
    #new_Transaction.name = 'admin' #request.POST['name'] # 'admin' #form.cleaned_data['name']
    #new_Transaction.save()
    
    #return HttpResponse(response, mimetype="application/json")

@login_required
def feed(request, url=None):
    #template = "userprofile/profile/overview.html"
    #validated = 'False'
    #data = { 'validated': validated }
    #return render_to_response(template, data, context_instance=RequestContext(request))

    #response, site, cachekey, sfeeds_obj, sfeeds_ids = initview(request)
#    if response:
#        return response

    #ctx = page_context(request, site, tag, user, (sfeeds_obj, sfeeds_ids))

    #response = render_to_response('feed/default/list.html', ctx, context_instance=RequestContext(request))

    # per host caching, in case the cache middleware is enabled
    #patch_vary_headers(response, ['Host'])
    singlequery = getsinglefeed(url);
    #_feed = feedparser.parse('http://www.channelnewsasia.com/rss/latest_cna_frontpage_rss.xml')
    _feed = feedparser.parse(singlequery.url);
    #if site.use_internal_cache vim user_feeds.html:
    #    cache_set(site, cachekey, response)
    ctx = {'feed':_feed,}
    response = render_to_response('feed/feeds.html', ctx, context_instance=RequestContext(request))
    return response


@login_required
def userfeed(request):
    documents = getuserfeeds(request.user.username)
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_Transaction = form.save(commit=False)
            new_Transaction.created_by = request.user.username #'admin'
            new_Transaction.url = form.cleaned_data['url']
            new_Transaction.name = form.cleaned_data['name']
            new_Transaction.save()
            form = FeedForm()
    else:
        form = FeedForm() # An unbound form

    ctx = {'form': form, 'documents': documents}
    response = render_to_response('feed/user_feeds.html', ctx, context_instance=RequestContext(request))
    return response



#    """
#    Main profile page
#    """
#    profile, created = Profile.objects.get_or_create(user=request.user)
#    validated = False
#    try:
#        email = EmailValidation.objects.get(user=request.user).email
#    except EmailValidation.DoesNotExist:
#        email = request.user.email
#        if email: validated = True

 #   template = "userprofile/profile/overview.html"
 #   data = { 'section': 'overview', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
 #            'email': email, 'validated': validated }
 #   return render_to_response(template, data, context_instance=RequestContext(request))


