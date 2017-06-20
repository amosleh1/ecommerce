from django.contrib import admin
from django import forms

from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib.sites.models import Site

from allauth.account.models import EmailAddress
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

from django.contrib.auth.forms import UserChangeForm

# To make the AllAuth EmailAddress Model inline/shown inside the UserProfile Model, inside the Admin Portal
class EmailAddressInline(admin.StackedInline):
	model = EmailAddress
	can_delete = False
	verbose_name_plural = 'Email Address'
	# to show one instance for the Email object per user
	max_num = 1


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ('email','first_name','last_name', 'password1', 'password2', 'phone','is_superuser','is_staff')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		return

@admin.register(UserProfile)
class UserAdmin(BaseUserAdmin):
	# To make the AllAuth EmailAddress Model inline/shown inside the UserProfile Model, inside the Admin Portal
	#form = MyUserChangeForm
	#add_form = UserCreationForm

	#inlines = (EmailAddressInline, )


	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ("email","first_name","last_name", "email_is_verified", "personal_info_is_completed", "is_superuser", )
	fieldsets =[
		("Profile Main Info",{"fields":[ "email", "first_name","last_name","is_superuser","is_staff" , "is_active" , "password"]}),
		("Other Info",{"fields":["phone", "nationality", "gender"]}),
		("Status Info",{"fields":["completion_level", "email_is_verified", "personal_info_is_completed","last_login","date_joined"]}),
	]
	list_display_links = ("email",)
	list_filter = ("is_superuser","email_is_verified",)
	search_fields = ("email", "first_name", "last_name",)
	readonly_fields=('email_is_verified','personal_info_is_completed', 'personal_info_is_completed','last_login','date_joined')
	ordering = ('email',)
	filter_horizontal = ()
	# This has afect on the fields used inside the Create_User form used in the ADMIN portal and its order inside the page
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email','first_name','last_name', 'password1', 'password2', 'phone','is_superuser','is_staff')}
		),
	)


# Ungregister the un-required Apps
admin.site.unregister(Group)
# the order fo the Site app inside the setting.py is important to not through an exception
admin.site.unregister(Site)
#Unregisteing the AllAuth Model as we will show it inline inside the userProfile as a single management UI
admin.site.unregister(EmailAddress)
# the order fo the allauth.socialaccount app inside the setting.py is important to not through an exception
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)