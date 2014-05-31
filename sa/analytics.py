from decimal import Decimal
import re, string

from obj_text_fragment import text_frag
from obj_word_analysis import word_analysis
from obj_word_summary import word_summary
from obj_sentence_analysis import sentence_analysis
from dataaccess import checkword, checkwords

from django.http import HttpResponse

def xhr_test(request):
    if request.is_ajax():
        message = "Hello AJAX"
    else:
        message = "Hello"
    return HttpResponse(message)

# initial input 
# called from /sa/analysis
def analytics_input(request):
    frag = text_frag()
    frag = split_text(frag, request)
    return frag


def split_text(txtfrag, request):
    words = request.split() #list of words separated at whitespace
    objsentences = sentence_analysis()
    punctuation = ['.', '!', '?', ';']
    fullsentence = ''
    txtfrag.text = request
    txtfrag.wa = word_analysis()
    txtfrag.wa.now = len(words) 
    txtfrag.sentences = []
    wis = []
    numbers = []
    for (counter, singleword) in enumerate(words):
        fullsentence += ' ' + singleword
        if singleword[-1:] in punctuation: #use string.punctuation but dunt want ,
            objsentences.text = fullsentence
            wis.append(singleword[:-1])
            objsentences.wa = wanalysis(wis) #word analysis
            if re.match('[0-9]', singleword[:-1]):
                numbers.append(singleword[:-1])
            objsentences.wa.summary.numbers = numbers
            txtfrag.sentences.append(objsentences)
            objsentences = sentence_analysis()
            fullsentence = ''
            wis = []
            numbers = []
        else:
            if re.match('[0-9]', singleword):
                numbers.append(singleword)
            wis.append(singleword)
    if fullsentence != '':
        objsentences.text = fullsentence
        objsentences.wa = wanalysis(wis) #word analysis
        objsentences.wa.summary.numbers = numbers
        txtfrag.sentences.append(objsentences)
    
    txtfrag.wa.nos = len(txtfrag.sentences)
    return txtfrag

def wanalysis(words):
   wa = word_analysis()
   wa.now = len(words)
   if wa.now == 1:
       wa.words = checkword(words[0])
   elif wa.now > 1:
       wa.words = checkwords(words)
   wa.summary = getsummary(wa)
   return wa

def fwanalysis(wa, words):
   return wa

def analytics_inputtest(text):
    frag = text_frag()
    frag.text = text
    frag = wanalysis2(frag)
    return frag

def wanalysis2(txtfrag):
   words = split_text(txtfrag, txtfrag.text)
   txtfrag.wa = word_analysis()
   txtfrag.wa.now = len(words)
   currentsentence = ''
   txtfrag.sentences = []
   txtfrag.events = []
   HaveEvent = False
   for word in words:
      currentsentence += ' ' + word
      if word[-1:] in string.punctuation:
          txtfrag.sentences.append(currentsentence)
          if HaveEvent:
             txtfrag.events.append(currentsentence)
             HaveEvent = False
          currentsentence = ''
      if re.match(r'[\d]', word):
          HaveEvent = True
          #txtfrag.events.append(currentsentence)
   txtfrag.sentences.append(currentsentence)
   currentsentence = ''
   txtfrag.sentencescount = len(txtfrag.sentences)
   txtfrag.eventscount = len(txtfrag.events)
   return txtfrag

def getsummary(wa):
   summary = word_summary()
   summary.npw = 0
   summary.nnw = 0
   summary.magnitude = Decimal('0.0')
   for (counter, word) in enumerate(wa.words):
     if word.type.name == 'positive':
        summary.npw += 1
        summary.magnitude += word.type.magnitude
     if word.type.name == 'negative':
        summary.nnw +=1
        summary.magnitude -= word.type.magnitude
     if word.type.name == 'passive':
        summary.who = wa.words[counter]
   return summary
