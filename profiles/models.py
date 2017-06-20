from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
# For the Phone Field
from django.core.validators import RegexValidator
# For the country Field
from django_countries.fields import CountryField

from django.conf import settings
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed, user_logged_in, password_changed
from django.db.models.signals import post_save
from django.contrib import messages
from allauth.account.models import EmailAddress


# --------------------------------- Related to Extending User Model ---------------------------------
''' 
This is a customized User Model
Based on info in page: https://docs.djangoproject.com/en/1.8/topics/auth/customizing/
Features Required:
	1- Any user to be created from the Admin portal will be:
		a- a super user who can access the Admin Portal
		b- will create for him an email inside the Allauth EmailAddress Model
		c- Will not need to verify his email
	2- Any Super User is a staff. This is done inside the model, by the is_staff property
	3- I have created the clean_email to check the uniquness of the email in all related app
	4- inside the Save method I have to remove the "if Commit:" as it was not true at all, for me later to create the emailAddress object
	5- Once a use is created, the email cannot be modified inside the admin portal. So I made it as read Only
'''

GENDER =(('man','Man'),('female','Female'))
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")


class UserManager(BaseUserManager):
	def create_user(self, email, first_name, last_name , password=None, **extra_fields):
		"""
        Creates and saves a User with the given email, names and password.
        """
		if not email:
			raise ValueError('Users must have an email address')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, last_name, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(email,
			first_name=first_name,
			last_name=last_name,
			password=password,
			is_superuser=True,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=30)
	last_name = models.CharField(_('last name'), max_length=30)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_admin = models.BooleanField(default=False)
	avatar = models.ImageField(upload_to='profile/Media/avatar/', null=True, blank=True)
	phone = models.CharField(validators=[PHONE_REGEX], max_length=16, blank=True, null=True) 
	# To Not have the Empty choice inside the gender field inside the template we set Blank as false and define a default value
	gender = models.CharField(max_length=40, blank=True, verbose_name=_(u'Gender'), choices=GENDER, default='') 
	nationality = CountryField(blank_label='(select country)',blank=True, default='')
	completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_(u'Profile completion percentage'))
	email_is_verified = models.BooleanField(default=False, verbose_name=_(u'Email is verified by user'))
	personal_info_is_completed = models.BooleanField(default=False, verbose_name=_(u'Personal info completed'))

	objects = UserManager()

	#List of the field names that will be prompted for when creating a user via the createsuperuser on CLI
	#This Attribute has no effect in other parts of Django, like creating a user in the admin.
	# However Although I see the fields in the CLI and I pt values, howver the values are
	REQUIRED_FIELDS = ['first_name', 'last_name']
	USERNAME_FIELD = 'email'

	class Meta:
		verbose_name = _('user profile')
		verbose_name_plural = _('user profiles')

	def get_full_name(self):
		'''
		Returns the first_name plus the last_name, with a space in between.
		'''
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
		Returns the short name for the user.
		'''
		return self.first_name

	def __str__(self): 
		return self.email

	@property
	def is_staff(self):
		#Is the user a member of staff?  Simplest possible answer: All admins are staff
		return self.is_admin

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

# This method used to modify the email_is_verified field once an email is confirmed by the user himself 
@receiver(email_confirmed, dispatch_uid="email_confirmed")
def set_email_confirmed(request,email_address, **kwargs):
	userProfile = UserProfile.objects.get(email=email_address.email)
	userProfile.email_is_verified = True
	userProfile.completion_level = userProfile.get_completion_level()
	userProfile.save()  
	if settings.DEBUG:
		print('Email set as verified')
	return

# This Method to notify the user once he change his password. By creating a message with level of 50 (from my choice)
# The site used for this method is https://docs.djangoproject.com/en/dev/ref/contrib/messages/#using-messages-in-views-and-templates
# The message will appear inside the template password_change.html
@receiver(password_changed)
def password_change_callback(sender, request, user, **kwargs):
    messages.add_message(request, 50, 'Password Was Changed Successfully !!')



'''
@receiver(user_signed_up, dispatch_uid="user_signed_up")
def create_new_profile(request, **kwargs):
	if settings.DEBUG:
		print('# ============ Signal fired: "user_signed_up" ============= #')
	if not request.user.is_authenticated():
		return
	user = kwargs['user']
	profile = UserProfile(user=user)
	profile.save()
	if settings.DEBUG:
		print('New profile created for user '+user.username)
	return


# Used this link for creating the below method
#https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
@receiver(post_save, sender=UserProfile)
def ensure_email_created(sender, **kwargs):
	# so we only do an action if the saved objed is newly saved. So 
	userProfile = kwargs.get('instance')
	if kwargs.get('created', False):
		email, email_created = EmailAddress.objects.get_or_create(user=userProfile, email= userProfile.email)
		#email = EmailAddress.objects.create(user=userProfile, email= userProfile.email)
		email.primary = True
		email.save()
		for key in kwargs:
			print ("another keyword arg: %s: %s" % (key, kwargs[key]))

'''