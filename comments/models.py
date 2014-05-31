from django.db import models

# Create your models here.

class objfeedback(models.Model): #Comment):
    title = models.CharField(max_length=300)
    value = models.CharField(max_length=1024)


