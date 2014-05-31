from models import rss, objdocument
from django.db.models import *

from datetime import datetime

from myproject.sa.dataaccess import *

def getuserfeeds(username):
   try:
       queryset = rss.objects.filter(created_by=username)
       return queryset
   except rss.DoesNotExist:
       return ''

def getsinglefeed(feed_id):
    try:
        singleresult = rss.objects.get(id=feed_id)
        return singleresult
    except rss.DoesNotExist:
        return ''

def createdocument(name, created_by, url, source, author, summary):
    new_doc = objdocument()
    new_doc.object = createobject(name, created_by, getclassid('document'))
    new_doc.url = url
    new_doc.source = source
    new_doc.author = author
    new_doc.summary = summary
    new_doc.save()
#    new_document = document()
#    new_document.created_by = created_by
#    new_document.url = url
#    new_document.name = name
#    new_document.timestamp = datetime.now()
#    new_document.save()
    return new_doc
