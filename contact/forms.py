from django import forms
from django.forms import ModelForm
from .models import Contact


'''
Form for Subitting a Contact Message
'''
class ContactForm(ModelForm): 
	
	class Meta:
		model = Contact
		fields = ['first_name', 'middle_name' ,'last_name' , 'phone' ,'email' ,'message' ,'message_type']