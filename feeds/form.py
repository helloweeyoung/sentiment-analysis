from django.forms import ModelForm
from django import forms
from models import rss


class FeedForm(ModelForm):
    class Meta:
        model = rss
        fields = ('url', 'name')

