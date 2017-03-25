from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#used for my customized created models
from .models import Category, Product

from .forms import SearchForm
#used for normalizing my search text
import re

# Create your views here.



def product_list(request, category_slug=None):
		"""
			For displying All products
		"""
		category = None
		categories = Category.objects.all()
		products = Product.objects.filter(is_published=True)
		if category_slug:
			category = get_object_or_404(Category, slug=category_slug)
			products = Product.objects.filter(categories__in=[category],is_published=True)
		# Pagination
		paginator = Paginator(products, 4) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			products = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			products = paginator.page(paginator.num_pages)
		# FInal Context Variables to Send
		context = {
			'category': category,
			'categories': categories,
			'products': products
		}
		return render(request,'product/list.html', context)


def product_detail(request, id, slug):
		product = get_object_or_404(Product,id=id,slug=slug,is_published=True)
		related_categories = product.categories.all()
		# Related products List has the same category as the current prodcut without repeatition. 
		related_products = Product.objects.filter(categories__in=list(related_categories)).exclude(id=product.id).distinct()
		
		# Final Context Variables to Send
		context = {
			'product': product,
			'related_products':related_products
		}
		return render(request,'product/detail.html', context)

def search_product(request):
		if request.method =='POST'
			form=SearchForm(request.POST)
				if form.is_valid():
					# Removing the start and last Spaces, replacing the spaces with Lines and using Regex to search on each word and finally remcing the duplicates 
					search_text_striped = form.cleaned_data('search_query').strip()
					search_text_normalized = re.sub(r' +',"|",search_text_striped)
					searched_product = Product.objects.filter(name__iregex=r'('+search_text_normalized+r')').distinct()
					print ("Result Objects:",searched_product)	
					context = {
						'searched_product': searched_product
					}

					return render(request,'product/search.html', context)

		else
			form=SearchForm
