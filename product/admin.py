from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	fieldsets =[
		("Product Main Info",{"fields":["name","slug","model","price"]}),
		("Prodcut Detailed Info", {"fields":["description", "image","created","updated","categories","is_published"]})
	]
	readonly_fields=(["created","updated"])
	list_display = ("name","model","created","updated","is_published")
	list_editable = ("is_published",)
	list_display_links = ("name","model")
	list_filter = ("is_published",)
	search_fields = ("name","categories__name")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	fieldsets =[
		("Category Main Info",{"fields":["name","slug"]}),
		("Category Detailed Info",{"fields":["description",]})
	]
	#readonly_fields=(["slug",])
	list_display = ("name","slug","description")
	list_display_links = ("name","slug")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}