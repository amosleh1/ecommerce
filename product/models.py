from django.db import models
from django.utils.timezone import now
from django.utils import timezone

from django.core.urlresolvers import reverse

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here. 

class Product(models.Model):

	name = models.CharField(max_length=200, help_text="Please Enter a Generic Name")
	model = models.CharField(max_length=70, blank=True, null=True)
	slug = models.SlugField(max_length=200, db_index=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='product/Media/%Y/%m/%d',blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(blank=True, null=True)
	show_stock = models.BooleanField(default=False, verbose_name="Show Stock Quantity?") 
	is_published = models.BooleanField(default=True, verbose_name="Publish?") 
	is_discounted = models.BooleanField(default=True, verbose_name="With Discount Offer?")
	discount_expire = models.DateTimeField(blank=True, null=True, verbose_name="Last Date for Discount")
	discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True,verbose_name="After Discount Price")
	created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	updated = models.DateTimeField(auto_now=True,blank=True, null=True)
	categories = models.ManyToManyField("Category",related_name="products")

	class Meta:
		ordering = ("name",)
		index_together = (('id', 'slug'),)

	def get_absolute_url(self):
		return reverse('product:product_detail',args=[self.id, self.slug])

	def clean(self):
		if self.is_discounted and (self.discounted_price is None or self.discounted_price == 0 or self.discount_expire is None or self.discount_expire < timezone.now()):
			raise ValidationError(_('Discount Price is not set correctty although Discount option is checked'))

#	def save(self, *args, **kwargs):
#		if (self.date_added is None):
#			self.date_added = now()
#		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.name




class Category(models.Model):

	name = models.CharField(max_length=150, help_text="Please Enter A Name", unique=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	image = models.ImageField(upload_to='category/Media/%Y/%m/%d',blank=True,null=True)
	description = models.TextField(blank=True, null=True)

	def get_absolute_url(self):
		return reverse('product:product_list_by_category', args=[self.slug])

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name


class Vacency(models.Model):

	title = models.CharField(max_length=200)
	job_summary = models.TextField(blank=True, null=True)
	location = models.TextField(blank=True, null=True)
	Responsibilities = models.TextField(blank=True, null=True)
	Requirements = models.TextField(blank=True, null=True)
	is_published = models.BooleanField(default=True, verbose_name="Publish?") 
	created_timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	expiration_date =  models.DateTimeField(blank=True, null=True, verbose_name="Last Date for Apply")


	class Meta:
		ordering = ("title",)

#	def save(self, *args, **kwargs):
#		if (self.date_added is None):
#			self.date_added = now()
#		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.title



class Career(models.Model):

	vacency = models.ForeignKey(Vacency)
	first_name = models.CharField(max_length=200)
	middle_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	nationality = models.CharField(max_length=200)
	birth_date = models.DateTimeField()
	phone = models.IntegerField(max_length=15, unique=True)
	email = models.EmailField(max_length=50)
	comment = models.CharField(max_length=500, help_text="Please Enter any comments")
	resume = models.ImageField(upload_to='product/Media/%Y/%m/%d',blank=True)
	applied_timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("first_name","last_name")

#	def save(self, *args, **kwargs):
#		if (self.date_added is None):
#			self.date_added = now()
#		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.name