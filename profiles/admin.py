from django.contrib import admin
from django import forms

from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserProfile
from allauth.account.models import EmailAddress


#For all Model options check link: https://docs.djangoproject.com/en/1.8/_modules/django/contrib/admin/options/

# ---------------------------------------------------- Related to User Profile Customization---------------------------------
''' 
This is a customized User Model Forms used inside the Admin Portal
Based on info in page: https://docs.djangoproject.com/en/1.8/topics/auth/customizing/
Features Required:
	1- users can only be created from the site signup page. So no users can be added form admin portal
	2- Users accounts can be removed or de-activated from the admin site
	3- Users data (other than the email address) can be modified from the admin portal
	2- Users' email cannot be modified inside the admin portal
	3- Super users can be created through the CLI or by creating a normal user then elavate his permission to a super user from the admin portal
	4- EmailAddresses can only be created/deleted/modified from the site (however we can only control is_verified, and is_primary). So no email controls can be done form admin portal

'''


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users from Admin Portal. Includes all the required
	fields, plus a repeated password. No change from the defaul code mentioned in the email"""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ('email', 'first_name', 'last_name' )

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
	class Meta:
		model = UserProfile
		fields = ('email', 'first_name', 'last_name', 'password', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]



# --------------------------------- Inline EmailAddress ---------------------------------
# As the Email address will be only added/deleted by the user site (and because user addition is also done from the use site). Use inline
# To make the AllAuth EmailAddress Model inline/shown inside the UserProfile Model, inside the Admin Portal
class EmailAddressInline(admin.StackedInline):
	model = EmailAddress
	can_delete = False
	verbose_name_plural = 'Email Address'
	# to show one instance for the Email object per user
	max_num = 1
	# update Allauth admin.py to hide the email field as it should be same as the user email entered
	fieldsets =[
		(None,{"fields":[ 'primary', 'verified' ]}),
	]



@admin.register(UserProfile)
class UserAdmin(BaseUserAdmin):
	# To make the AllAuth EmailAddress Model inline/shown inside the UserProfile Model, inside the Admin Portal
	form = UserChangeForm
	add_form = UserCreationForm
	inlines = (EmailAddressInline,)

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ("email","first_name","last_name", "email_is_verified", "is_active", "is_superuser", )
	fieldsets =[
		("Profile Main Info",{"fields":[ "email", "first_name","last_name","is_superuser", "is_active" , "password"]}),
		("Other Info",{"fields":["phone", "nationality", "gender"]}),
		("Status Info",{"fields":["completion_level", "email_is_verified", "personal_info_is_completed","last_login","date_joined"]}),
	]
	list_display_links = ("email",)
	list_editable = ('is_superuser','is_active')
	list_filter = ("is_superuser","email_is_verified",)
	search_fields = ("email", "first_name", "last_name",)
	# I made the Email field read only so we do not have to worry about the change to an existing email address.
	readonly_fields=('email','completion_level','email_is_verified','personal_info_is_completed','last_login','date_joined')
	ordering = ('email',)
	filter_horizontal = ()
	# This has afect on the fields used inside the Create_User form used in the ADMIN portal and its order inside the page
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email','first_name','last_name', 'password1', 'password2',)}
		),
	)
	#Disable adding an admin inside the Admin Portal. So we force the addition of a user or super user through the CLI or the AllAuth Signup
	def has_add_permission(self, request):
		return False



# -------------------------------------------------------- Ungregister the un-required Apps----------------------------------------
#Unregisteing the AllAuth Model as we will show it inline inside the userProfile as a single management UI
admin.site.unregister(EmailAddress)
# Un-registering the Default Group Model as it is not required in our App
admin.site.unregister(Group)
# the order fo the Site app inside the setting.py is important to not through an exception
admin.site.unregister(Site)
# the order fo the allauth.socialaccount app inside the setting.py is important to not through an exception
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)


'''
# --------------------------------- Customizing the AllAuth EmailAddress Model inside the Admin Portal---------------------------------

The gaol is to block any addition/deletion for the emails, So we make sure as much we can to control it from the userProfile
Also we have mase the Email field read only to make.So the rule is to re-create the account if email to be changed or to go thruogh the AllAuth way

admin.site.unregister(EmailAddress)
@admin.register(EmailAddress)
class MyCustomEmailAddress(admin.ModelAdmin):
	model = EmailAddress
	list_display = ('user','email','primary', 'verified')
	#raw_id_fields = ('user')
	search_fields = ("email",)
	#Disable Editing Email From Admin Portal
	readonly_fields=('email','user')
	list_filter = ('primary', 'verified')
	list_editable = ('primary','verified')
	ordering = ('email',)
	show_full_result_count = True
	#Disable adding/Deleting an Email inside the Admin Portal. So we force the addition of a user or super user through the CLI or the AllAuth Signup
	def has_add_permission(self, request):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	#Remove the Actions option inside the Admin "Email Address" List
	def get_actions(self, request):
		return

'''











'''
# --------------------------------- Inline EmailAddress ---------------------------------
# To make the AllAuth EmailAddress Model inline/shown inside the UserProfile Model, inside the Admin Portal
class EmailAddressInline(admin.StackedInline):
	model = EmailAddress
	can_delete = False
	verbose_name_plural = 'Email Address'
	# to show one instance for the Email object per user
	max_num = 1
	# update Allauth admin.py to hide the email field as it should be same as the user email entered
	fieldsets =[
		(None,{"fields":[ 'primary', 'verified' ]}),
	]
#Unregisteing the AllAuth Model as we will show it inline inside the userProfile as a single management UI
admin.site.unregister(EmailAddress)

'''


'''
# Below is my customer UserCreationForm/save and UserCreationForm/clean_email methods once adding a use inside admin portal is activated. Where I need to check if an email inside EMAIL address model or user model exists already

	# I have created this method to check if the entered email is unique in both EmailAddress App and UserProfile App
	# this method will be called automatically once the form get checked against the clean logic
	def clean_email(self):
		allauth_email = EmailAddress.objects.filter(email= self.cleaned_data.get("email")).first()
		user_email = UserProfile.objects.filter(email= self.cleaned_data.get("email")).first()
		if allauth_email == None and user_email == None:
			return
		else:
			raise forms.ValidationError("Email is used either inside Email Address App or User profile")

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		# I have descided to make the created user inside the Admin portal Always a super admin and hided the field inside the create form by modifying add_fieldsets
		user.is_superuser = True
		# Note: I had to remove the if statment related to checking the commit value. As it was never TRUE for me to create the email related object!!!!
		user.save()
		#Ceating the related EmailAddress 
		email = EmailAddress.objects.create(user=user, email= user.email)
		email.primary = True
		email.verified = True
		email.save()
		return user
'''
