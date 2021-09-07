from django.shortcuts import render
from django.views.generic.edit import FormView

from app.forms import ContactForm
# Create your views here.

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'