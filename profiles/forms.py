from django import forms
from django.http import Http404
from django.contrib.auth.models import User
from .models import UserProfile


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		# note that email and passwords field will show in the form (by default comming from AllAuth). 
		#Below include the additional fields
		fields = ('first_name', 'last_name', 'phone',)
	#Modify the default the signup method of the User model from AllAuth
	def signup(self, request, userProfile):
		# ALl original fields exists in User model will be saved without the need to expilicity mentioning it below
		userProfile.phone = self.cleaned_data['phone']
		userProfile.save()
	'''
	# IN this method I will dectate which filed inside this form is required wihtout the need to modify the User Model (By removing blank=true and null=true). Which help in keeping the DB as it is.
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		return
	'''

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # note that username, email and passwords field will show in the form comming from AllAuth. Below is an extension
        fields = ('first_name', 'last_name','email','phone', 'nationality', 'gender', )

