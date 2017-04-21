from django.db import models
from django.utils.timezone import now
from django.utils import timezone
# For the Slug Field
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
# For the country Field
from django_countries.fields import CountryField
#Used for the Telephone Field validation
from django.core.validators import RegexValidator

from django.utils.safestring import mark_safe


class Vacancy(models.Model):

	title = models.CharField(max_length=150, unique=True,db_index=True)
	slug = models.CharField(max_length=150, unique=True)
	job_summary = models.TextField(blank=True, null=True)
	location = CountryField(blank_label='(select country)')
	responsibilities = models.TextField(blank=True, null=True)
	requirements = models.TextField(blank=True, null=True)
	is_published = models.BooleanField(default=True, verbose_name="Publish?") 
	created_timestamp = models.DateField( auto_now_add=True)


	def get_absolute_url(self):
		return reverse('career:vacancy_detail', args=[self.id, self.slug])
		#return "/vacancy/%s/" % self.slug

	class Meta:
		ordering = ("is_published","title",)
		index_together = (('id', 'slug'),)
		verbose_name = 'Vacancy'
		verbose_name_plural = 'Vacancies'

	def save(self, *args, **kwargs):
		#if (self.date_added is None):
		#	self.date_added = now()
		# for replacing all spaces inside the titile and copy the result to the Slug before saving
		self.slug = slugify(self.title)
		# for preserving line breaks inside
		#self.responsibilities = self.responsibilities.replace("\n", "<br/>")
	
		super(Vacancy, self).save(*args, **kwargs)

	def __str__(self):
		return self.title



class Resume(models.Model):

	phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', 
		message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")

	vacancy = models.ForeignKey(Vacancy)
	first_name = models.CharField(max_length=150)
	middle_name = models.CharField(max_length=150, blank=True, null=True)
	last_name = models.CharField(max_length=150)
	nationality = models.CharField(max_length=150,)
	birth_date = models.DateField()
	phone = models.CharField(validators=[phone_regex], max_length=16) 
	email = models.EmailField(max_length=50)
	comment = models.CharField(max_length=500, help_text="Please Enter any comments", blank=True, null=True)
	resume_file = models.FileField(upload_to='career/%Y/%m/%d/')
	applied_timestamp = models.DateField(auto_now_add=True);

	class Meta:
		ordering = ("applied_timestamp",)
#	def save(self, *args, **kwargs):
#		if (self.date_added is None):
#			self.date_added = now()
#		super(career, self).save(*args, **kwargs)