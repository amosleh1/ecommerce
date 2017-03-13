from django.db import models

# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=150, help_text="Please Enter a Generic Name")
	model = models.CharField(max_length=70, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	Price = models.IntegerField()
	is_published = models.BooleanField(default=False, verbose_name="Publish?") 
	Date_Added = models.DateTimeField() 

	def __str__(self):
		return self.name