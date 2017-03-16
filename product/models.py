from django.db import models
from django.utils.timezone import now

# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=200, help_text="Please Enter a Generic Name")
	model = models.CharField(max_length=70, blank=True, null=True)
	slug = models.SlugField(max_length=200, db_index=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='product/Media/%Y/%m/%d',blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(blank=True, null=True)
	available = models.BooleanField(default=True)
	is_published = models.BooleanField(default=False, verbose_name="Publish?") 
	created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	updated = models.DateTimeField(auto_now=True,blank=True, null=True)
	categories = models.ManyToManyField("Category",related_name="products")
	
	class Meta:
		ordering = ("name",)
		index_together = (('id', 'slug'),)
#	def save(self, *args, **kwargs):
#		if (self.date_added is None):
#			self.date_added = now()
#		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=150, help_text="Please Enter A Name", unique=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	description = models.TextField(blank=True, null=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name