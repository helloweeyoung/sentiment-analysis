#-*- coding: UTF-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.template import RequestContext

# Create your views here.

from models import *
from form import *
from analytics import analytics_input, analytics_inputtest
from obj_text_fragment import text_frag
from dataaccess import gethistory, getreaddocuments, getdocument

from myproject.charting.templatetags.chart import *
from myproject.comments.views import *

from myproject.scrape.views import *

def xhr_test(request):
    if request.is_ajax():
        message = "Hello AJAX"
    else:
        message = "Hello"
    return HttpResponse(message)

#@login_required
def text_input(request):
    if request.method == 'POST': # If the form has been submitted...
        form = saForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            print "using form"
            new_Transaction = form.save(commit=False)
            new_Transaction.save()
            text = form.cleaned_data['Text']
            form = saForm()
            return render_to_response('sa/text_analysis.html', {
                'form': form,
                'text': text,
            })

            # return HttpResponseRedirect('input', {'form': form}) # Redirect after POST
    else:
        form = saForm() # An unbound form

    return render_to_response('sa/text_fragment.html', {
        'form': form,
    })

#@login_required
def text_analysis(request):
    txtfrag = text_frag()
    if request.method == 'POST': # If the form has been submitted...
        form = saForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            txtfrag = analytics_input(form.cleaned_data['name'])
            new_Transaction = form.save(commit=False)
            new_Transaction.created_by = request.user.username #'admin'
            new_Transaction.magnitude = '1.0'#txtfrag.wa.summary.magnitude 
            new_Transaction.save()
            #text = form.cleaned_data['Text']
            form = saForm()
            #return HttpResponseRedirect('analysis') # Redirect after POST
    else:
        form = saForm() # An unbound form
    return render_to_response('sa/text_analysis.html', {
        'form': form,
	'txtfrag': txtfrag,
    }, context_instance=RequestContext(request))

@login_required
def text_history(request):
    txtfrag = gethistory(request.user.username)   
    docs = getreaddocuments(request.user.username)
    return render_to_response('sa/user_history.html', {
        'txtfrag': txtfrag, 
        'docs': docs,
    }, context_instance=RequestContext(request))


def feedback(request):
    sa_comment = getfeedback(1)
    return render_to_response('sa/feedback.html', {
        'sa_comment': sa_comment,
    },  context_instance=RequestContext(request))

def test(request):
    test = getsource('http://www.channelnewsasia.com/stories/singaporelocalnews/view/1069917/1/.html')
    visibletext = getvisibletext(test)
    visibletext = analytics_inputtest(visibletext);
    return render_to_response('sa/test.html', {
        'test': test, 'visibletext':visibletext,
    },  context_instance=RequestContext(request))

def opendocument(request, document=None):
    doc = getdocument(document)
    return render_to_response('sa/document.html', {
        'doc': doc,
    },  context_instance=RequestContext(request))

