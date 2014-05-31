from models import *
from django.db.models import *

def getafeedback(id):
   try:
       queryset = objfeedback.objects.get(id=id)
       return queryset
   except objfeedback.DoesNotExist:
       return ''

