from django.contrib import admin
from .models import Product, Category


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	fieldsets =[
		("Product Main Info",{"fields":["name","model","price","image","is_published"]}),
		("Prodcut Detailed Information", {"fields":["description","stock", "show_stock" ,"categories"]}),
		("Product Discount",{"fields":["is_discounted","discounted_price","discount_expire"]})
	]
	#readonly_fields=(["created","updated"])
	list_display = ("name","model","price","updated","is_published","updated")
	list_editable = ("is_published",)
	list_display_links = ("name",)
	list_filter = ("is_published", "categories__name")
	search_fields = ("name","categories__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	fieldsets =[
		("Category Main Info",{"fields":["name","description","image"]}),
	]
	list_display = ("name","description")
	list_display_links = ("name",)
	search_fields = ("name",)

