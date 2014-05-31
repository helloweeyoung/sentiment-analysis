from models import *
from django.db.models import *

from datetime import datetime

from myproject.feeds.models import objdocument

def checkword(request):
    try:
        queryset = word.objects.filter(name=request)
        return queryset
    except word.DoesNotExist:
        return ''

def checkwords(request):
    try:
       querystring = populateparams(request)
       queryset = word.objects.filter(name__regex=querystring)
       return queryset
    except word.DoesNotExist:
        return ''


def populateparams(params):
    #return r'^(happy|joy)'
    return r''.join(['^' + param + '$|' for param in params])[:-1]

def gethistory(username):
   try:
       queryset = textfragment.objects.filter(created_by=username)
       return queryset
   except textfragment.DoesNotExist:
       return ''

def getreaddocuments(username):
   try:
       queryset = objdocument.objects.filter(object__created_by=username)
      # queryset = object.objects.filter(created_by=username).filter(classid=getclassid('document'))
       return queryset
   except objdocument.DoesNotExist:
       return ''

def getdocument(doc_id):
   try:
       queryset = objdocument.objects.get(id=doc_id)
      # queryset = object.objects.filter(created_by=username).filter(classid=getclassid('document'))
       return queryset
   except objdocument.DoesNotExist:
       return ''

def getclassid(classname):
   try:
       queryset = objectclass.objects.get(name=classname)
       return queryset
   except objectclass.DoesNotExist:
       return 0

def createobject(name, created_by, classid):
   New_Obj = object()
   New_Obj.name = name
   New_Obj.created_by = created_by
   New_Obj.timestamp = datetime.now()
   New_Obj.classid = classid
   New_Obj.save()
   return New_Obj
