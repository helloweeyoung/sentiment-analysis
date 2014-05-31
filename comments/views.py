#-*- coding: UTF-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.template import RequestContext

from models import *
from dataaccess import *

def getfeedback(id):
    return getafeedback(id)

