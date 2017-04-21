from django import forms

# Required for the Career Forms
from django.forms import ModelForm, Textarea,TextInput
from .models import Resume
from django.utils.translation import ugettext_lazy as _
from django.forms.extras import SelectDateWidget
import datetime
import os
from django.core.exceptions import ValidationError
'''
Form for Subitting a Job
'''
class ResumeForm(ModelForm): 
	
	class Meta:
		model = Resume
		fields = ['first_name', 'middle_name' ,'last_name' ,'nationality' ,'birth_date' ,'phone' ,'email' ,'comment' ,'resume_file']   # Or a list of the fields that you want to include in your form without it will get Error  "Creating a ModelForm without either the 'fields'"
		#years_to_display = range(datetime.datetime.now().year - 100, datetime.datetime.now().year)

		#widgets = {
          #  'comment': Textarea(attrs={'cols': 60, 'rows': 6}),
          #  'birth_date': SelectDateWidget(years=years_to_display),
         #   'phone': TextInput(attrs={'placeholder': '+XXX YYY YYY'}),
        #}

		#labels = {
		#	'resume_file': _('Upload Resume'),
		#}

	def clean_resume_file(self):
		"""
			SValidate of the sub,itted file use an acceptable extension + an acceptable size
		"""
		file = self.cleaned_data.get("resume_file", False)
		# check file extension 
		ext = os.path.splitext(file.name)[1]  # [0] returns extension only
		valid_extensions = ['.pdf', '.doc', '.docx']
		if not ext.lower() in valid_extensions:
			raise ValidationError(u'Unsupported file extension.')
		# check file size
		if file._size > 4*1024*1024:
			raise ValidationError("file size is too large ( > 4mb )")

		return file

