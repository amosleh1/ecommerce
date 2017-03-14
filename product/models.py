from django.db import models

# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=150, help_text="Please Enter a Generic Name")
	model = models.CharField(max_length=70, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	price = models.IntegerField()
	is_published = models.BooleanField(default=False, verbose_name="Publish?") 
	date_added = models.DateTimeField(blank=True, null=True) 
	categories = models.ManyToManyField("Category",related_name="products")
	
	def __str__(self):
		return self.name

class Image(models.Model):
	name = models.CharField(max_length=150, help_text="Please Enter a Generic Name")
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=150, help_text="Please Enter A Name", unique=True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name