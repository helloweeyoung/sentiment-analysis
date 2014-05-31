# Create your views here.
import urllib2
import re
import string

from BeautifulSoup import BeautifulSoup

from obj_scrape import obj_scrape

def getsource(url):
   page = urllib2.urlopen(url)
   soup = BeautifulSoup(page)
   return soup

def visible(element):
   if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
   elif re.match('<!--.*-->', str(element)):
        return False
   return True

def getvisibletext(soup):
   texts = filter(visible, soup.findAll(text=True)) #clearunwanted(soup.findAll(text=True)) #filter(visible, soup.findAll(text=True))
   justtext = ''
   for text in texts:
       justtext += splitandjoin('<.+>|</.+>', text)
   #sentences = []
   #sentences = getsentence(justtext)
   obj_scrape.text = justtext
  # obj_scrape.words = getsentence(justtext)
   return obj_scrape.text #getsentence(justtext) #sentences

def splitandjoin(regex, sentence):
   return re.sub(regex, ' ', sentence)

def clearunwanted(texts):
   texts = filter(visible, texts)
   for text in texts:
      text = splitandjoin('<.+>|</.+>', text)
   return texts

def getsentence(walloftext):
   return walloftext.split() #.split('.')
