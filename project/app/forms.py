
from django import forms
from django.db.models import fields
from app import models
from .models import Contact


class ContactForm(forms.ModelForm):
        
    class Meta:
        model = Contact
        fields = "__all__"

