from django.shortcuts import render
from .models import Product

# Create your views here.
def list_products(request):
	"""
		For displying All products
	"""
	products = Product.objects.all()
	context = {
		'products':products,

	}
	return render(request, "list.html", context)