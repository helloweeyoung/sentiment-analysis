from django.db import models
from django.contrib.comments.models import Comment

# Create your models here.
class yobj(models.Model):
    name = models.CharField(max_length=1024)
    created_by = models.CharField(max_length=1024, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class mobj(yobj):
    magnitude = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        abstract = True
  
class textfragment(mobj):
    def __unicode__(self):
        return self.name

class emotype(mobj):
    def __unicode__(self):
        return self.name

class word(mobj):
    type = models.ForeignKey(emotype)
    def __unicode__(self):
        return self.name

class objectclass(yobj):
    def __unicode__(self):
        return self.name

class object(yobj):
    classid = models.ForeignKey(objectclass)
    def __unicode__(self):
        return self.name

#class linguist(yobj):
#    classid = models.ForeignKey(objectclass)
#    def __unicode__(self):
#        return self.name

#class lingtype(yobj):
#    linguist =  models.ForeignKey(linguist)
#    def __unicode__(self):
#        return self.name

#class lingrelationshipclass(yobj):
#   parent = models.CharField(max_length=1024)
#   child = models.CharField(max_length=1024)
#   def __unicode__(self):
#        return self.name 

#class lingrelationship(yobj):
#    lingparent =  models.ForeignKey(linguist)
#    lingchild =  models.ForeignKey(linguist)
#    relclass = models.ForeignKey(lingrelationshipclass)
#    def __unicode__(self):
#        return self.name

#class objdocument(models.Model):
#    objectid = models.ForeignKey(object)
#    url = models.URLField(verify_exists=False, max_length=1024, null=True)
#    body = models.TextField(null=True)
#    def __unicode__(self):
#        return self.name 

class relationshipclass(yobj):
    def __unicode__(self):
        return self.name

class relationships(models.Model):
    relationship = models.ForeignKey(relationshipclass)
    parent = models.CharField(max_length=1024)
    child = models.CharField(max_length=1024)
    def __unicode__(self):
        return self.name

RELATIONSHIP_CHOICES = (
        ('P', 'Parent'),
        ('C', 'Child'),
)

class relationshipsobj(models.Model):
    relationship = models.ForeignKey(relationships)
    object = models.ForeignKey(object)
    parentorchild = models.CharField(max_length=1, choices=RELATIONSHIP_CHOICES)
    def __unicode__(self):
        return self.name

class linguistictype(yobj):
   objclass =  models.ForeignKey(objectclass)
   def __unicode__(self):
        return self.name

class role(yobj):
    def __unicode__(self):
        return self.name

class linguisticrelationship(yobj):
    def __unicode__(self):
        return self.nam

class linguisticrelationshiprole(models.Model):
   relationship =  models.ForeignKey(linguisticrelationship)
   role =  models.ForeignKey(role)
   type = models.ForeignKey(linguistictype)
   def __unicode__(self):
        return self.nam

class lingrelationshipsobj(models.Model):
    relationship = models.ForeignKey(linguisticrelationship)
    object = models.ForeignKey(object)
    role =  models.ForeignKey(linguisticrelationshiprole)
    def __unicode__(self):
        return self.name

class objlinguistic(models.Model):
    object = models.ForeignKey(object)
    lingclass = models.ForeignKey(linguistictype)
    def __unicode__(self):
        return self.name

    
