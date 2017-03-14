from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	fieldsets =[
		("Product Main Info",{"fields":["name","model","price"]}),
		("Prodcut Detailed Info", {"fields":["description","date_added","categories","is_published"]})
	]

	readonly_fields=(["date_added"])
	list_display = ("name","model","date_added","is_published")
	list_editable = ("is_published",)
	list_display_links = ("name","model")
	list_filter = ("is_published",)
	search_fields = ("name","categories__name")


# Register your models here.
admin.site.register(Category)