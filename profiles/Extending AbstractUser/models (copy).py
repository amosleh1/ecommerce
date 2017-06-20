from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# For the Phone Field
from django.core.validators import RegexValidator
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
#from django.conf import settings
#from django.dispatch import receiver
#from allauth.account.signals import user_signed_up, email_confirmed, user_logged_in
#from allauth.account.models import EmailAddress


GENDER =(('man','Man'),('female','Female'))
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")



class UserProfile(AbstractUser):
	self.email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
	phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True) 
	# To Not have the Empty choice inside the gender field inside the template we set Blank as false and define a default value
	gender = models.CharField(max_length=40, blank=True, verbose_name=_(u'Gender'), choices=GENDER, default='') 
	nationality = CountryField(blank_label='(select country)',blank=True, default='')
	#avatar = models.ImageField(upload_to='userprofiles/avatars', null=True, blank=True, verbose_name=_(u"Avatar"))
	completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'Profile completion percentage'))
	email_is_verified = models.BooleanField(default=False, verbose_name=_(u'Email is verified'))
	personal_info_is_completed = models.BooleanField(default=False, verbose_name=_(u'Personal info completed'))
	#List of the field names that will be prompted for when creating a user via the createsuperuser on CLI
	REQUIRED_FIELDS = ['email','first_name', 'last_name']
	USERNAME_FIELD = 'email'


	class Meta:
		verbose_name=_(u'User profile')
		verbose_name_plural = _(u'User profiles')

	def get_completion_level(self):
		completion_level = 0
		if self.email_is_verified:
			completion_level += 50
		if self.personal_info_is_completed:
			completion_level += 50
		return completion_level

	def update_completion_level(self):
		self.completion_level = self.get_completion_level()
		self.save()
		return

