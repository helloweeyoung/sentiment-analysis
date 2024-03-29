# -*- coding: utf-8 -*-

"""
feedjack
Gustavo Picón
fjlib.py
"""

from django.conf import settings
from django.db import connection
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.utils.encoding import smart_unicode

from models import Site, Tag, Feed, Post
from fjcache import hostcache_get, hostcache_set
from fjcloud import getcloud

def sitefeeds(siteobj):
    """ Returns the active feeds of a site.
    """
    return siteobj.subscriber_set.filter(is_active=True).select_related()
    #return [subscriber['feed'] \
    #  for subscriber \
    #  in siteobj.subscriber_set.filter(is_active=True).values('feed')]

def getquery(query):
    """ Performs a query and get the results.
    """
    try:
        conn = connection.cursor()
        conn.execute(query)
        data = conn.fetchall()
        conn.close()
    except:
        data = []
    return data

def get_extra_content(site, sfeeds_ids, ctx):
    """ Returns extra data useful to the templates.
    """

    # get the subscribers' feeds
    if sfeeds_ids:
        basefeeds = Feed.objects.filter(id__in=sfeeds_ids)
        try:
            ctx['feeds'] = basefeeds.order_by('name').select_related()
        except:
            ctx['feeds'] = []

        # get the last_checked time
        try:
            ctx['last_modified'] = basefeeds.filter(\
              last_checked__isnull=False).order_by(\
              '-last_checked').select_related()[0].last_checked.ctime()

        except:
            ctx['last_modified'] = '??'
    else:
        ctx['feeds'] = []
        ctx['last_modified'] = '??'
    ctx['site'] = site
    ctx['media_url'] = '%s/feedjack/%s' % (settings.MEDIA_URL, site.template)

def get_posts_tags(object_list, sfeeds_obj, user_id, tag_name):
    """ Adds a qtags property in every post object in a page.
    
    Use "qtags" instead of "tags" in templates to avoid innecesary DB hits.
    """
    tagd = {}
    user_obj = None
    tag_obj = None
    tags = Tag.objects.extra(\
      select={'post_id':'%s.%s' % (\
        connection.ops.quote_name('feedjack_post_tags'), \
        connection.ops.quote_name('post_id'))}, \
      tables=['feedjack_post_tags'], \
      where=[\
        '%s.%s=%s.%s' % (\
          connection.ops.quote_name('feedjack_tag'), \
          connection.ops.quote_name('id'), \
          connection.ops.quote_name('feedjack_post_tags'), \
          connection.ops.quote_name('tag_id')), \
        '%s.%s IN (%s)' % (\
          connection.ops.quote_name('feedjack_post_tags'), \
          connection.ops.quote_name('post_id'), \
          ', '.join([str(post.id) for post in object_list]))])
    for tag in tags:
        if tag.post_id not in tagd:
            tagd[tag.post_id] = []
        tagd[tag.post_id].append(tag)
        if tag_name and tag.name == tag_name:
            tag_obj = tag
    subd = {}
    for sub in sfeeds_obj:
        subd[sub.feed.id] = sub
    for post in object_list:
        if post.id in tagd:
            post.qtags = tagd[post.id]
        else:
            post.qtags = []
        post.subscriber = subd[post.feed.id]
        if user_id and int(user_id) == post.feed.id:
            user_obj = post.subscriber
    return user_obj, tag_obj

def getcurrentsite(http_post, path_info, query_string):
    """ Returns the site id and the page cache key based on the request.
    """
    url = u'http://%s/%s' % (smart_unicode(http_post.rstrip('/')), \
      smart_unicode(path_info.lstrip('/')))
    pagecachekey = '%s?%s' % (smart_unicode(path_info), \
      smart_unicode(query_string))
    hostdict = hostcache_get()

    if not hostdict:
        hostdict = {}
    if url not in hostdict:
        default, ret = None, None
        for site in Site.objects.all():
            if url.startswith(site.url):
                ret = site
                break
            if not default or site.default_site:
                default = site
        if not ret:
            if default:
                ret = default
            else:
                # Somebody is requesting something, but the user didn't create
                # a site yet. Creating a default one...
                ret = Site(name='Default Feedjack Site/Planet', \
                  url='www.feedjack.org', \
                  title='Feedjack Site Title', \
                  description='Feedjack Site Description. ' \
                    'Please change this in the admin interface.')
                ret.save()
        hostdict[url] = ret.id
        hostcache_set(hostdict)

    return hostdict[url], pagecachekey

def get_paginator(site, sfeeds_ids, page=0, tag=None, user=None):
    """ Returns a paginator object and a requested page from it.
    """

    if tag:
        try:
            localposts = Tag.objects.get(name=tag).post_set.filter(\
              feed__in=sfeeds_ids)
        except:
            raise Http404
    else:
        localposts = Post.objects.filter(feed__in=sfeeds_ids)

    if user:
        try:
            localposts = localposts.filter(feed=user)
        except:
            raise Http404
#    if site.order_posts_by == 2:
#        localposts = localposts.order_by('-date_created', '-date_modified')
#    else:
#        localposts = localposts.order_by('-date_modified')

    paginator = Paginator(localposts.select_related(), 1)#site.posts_per_page)
    try:
        object_list = paginator.page(page)
    except InvalidPage:
        if page == 0:
            object_list = []
        else:
            raise Http404
    return (paginator, object_list)

def page_context(request, site, tag=None, user_id=None, sfeeds=None):
    """ Returns the context dictionary for a page view.
    """
    sfeeds_obj, sfeeds_ids = sfeeds
    try:
        page = int(request.GET.get('page', 0))
    except ValueError:
        page = 0
    paginator, object_list = get_paginator(site, sfeeds_ids, page=page, tag=tag, user=user_id)
    if object_list:
        # This will hit the DB once per page instead of once for every post in
        # a page. To take advantage of this the template designer must call
        # the qtags property in every item, instead of the default tags
        # property.
        user_obj, tag_obj = get_posts_tags(object_list, sfeeds_obj, user_id, tag)
    else:
        user_obj, tag_obj = None, None
    if page > 0:
        has_next = paginator.page(page).has_next()
        has_previous = paginator.page(page).has_previous()
    else:
        if paginator.num_pages > 1:
            has_next = True
        else:
            has_next = False
            has_previous = False
    ctx = {
#         'data': 'data'
        'object_list': object_list,
        'is_paginated': paginator.num_pages > 1, #from paginator.pages
        'results_per_page': 1,#site.posts_per_page,
        'has_next': has_next,
        'has_previous': has_previous,
        'page': page + 1,
        'next': page + 1,
        'previous': page - 1,
        'pages': paginator.num_pages, #from paginator.pages,
        'hits' : paginator.count, #from paginator.hits,
    }
    get_extra_content(site, sfeeds_ids, ctx)
    ctx['tagcloud'] = getcloud(site, user_id)
    ctx['user_id'] = user_id
    #ctx['user'] = user_obj
    ctx['tag'] = tag_obj
    ctx['subscribers'] = sfeeds_obj
    return ctx


#~
