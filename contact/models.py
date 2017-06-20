from django.db import models

from django.utils.timezone import now
from django.utils import timezone
# For the country Field
from django_countries.fields import CountryField
#Used for the Telephone Field validation
from django.core.validators import RegexValidator



class Contact(models.Model):
	CHOICES = (('Business Offer','Business Offer'), ('Complain','Complain'),('Question','Question'))
	phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', 
		message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")

	first_name = models.CharField(max_length=150)
	middle_name = models.CharField(max_length=150, blank=True, null=True)
	last_name = models.CharField(max_length=150)
	phone = models.CharField(validators=[phone_regex], max_length=16) 
	email = models.EmailField(max_length=50, blank=True, null=True)
	message = models.CharField(max_length=500, help_text="Please Enter your message")
	message_type = models.CharField(max_length=30, choices=CHOICES)
	applied_timestamp = models.DateField(auto_now_add=True);

	class Meta:
		ordering = ("applied_timestamp",)

	def __str__(self):
		return self.message_type
