from django.shortcuts import render, get_object_or_404
# used for pagnation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#used for my customized created models
from .models import Category, Product
from cart.forms import CartAddProductForm

from .forms import SearchForm
#used for normalizing my search text
import re




def product_list(request, category_slug=None):
		"""
			For displying All products and Categories
		"""
		#for listing Categories othat has at least one published product
		categories = Category.objects.filter(products__is_published=True).distinct()
		#List all products
		page_list = Product.objects.filter(is_published=True)
		show_count = None
		category = None
		

		# If this is a GET request then process the Form data
		if request.method == 'GET':
			# Create a form instance and populate it with data from the request (binding):
			form=SearchForm(request.GET)
			if form.is_valid():
				show_count = form.cleaned_data['show_count']
			

		# List Prodcuts based on Category
		if category_slug:
			category = get_object_or_404(Category, slug=category_slug)
			page_list = Product.objects.filter(categories__in=[category],is_published=True)
		
		# handeling Paganation & Items count per page
		if show_count:
			paginator = Paginator(page_list, show_count)
		else:
			 paginator = Paginator(page_list, 10)
			 show_count = 10
		page = request.GET.get('page')
		try:
			page_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			page_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			page_list = paginator.page(paginator.num_pages)
		
		# Fixing the proplem of the reptitave Page attribute in URL when using the paging links
		url_without_page = request.GET.copy()
		if 'page' in url_without_page:
			del url_without_page['page']

		# FInal Context Variables to Send
		context = {
			'category': category,
			'categories': categories,
			'page_list': page_list,
			'url_without_page':url_without_page,
			'show_count':show_count,
		}
		return render(request,'product/product_list.html', context)


def promotion_list(request, category_slug=None):
		"""
			For displying ONly Discounted and Featured products and Categories
		"""
		#for listing Categories on the lift side of the page
		categories = Category.objects.filter(products__is_discounted=True).distinct()
		products = Product.objects.filter(is_published=True).filter(is_discounted=True)
		
		# FInal Context Variables to Send
		context = {
			'categories': categories,
			'products': products,
		}
		return render(request,'product/promotion_list.html', context)




def category_list(request):
		"""
			For displying All Categories
		"""
		#for listing Categories othat has at least one published product
		page_list = Category.objects.filter(products__is_published=True).distinct()

		# Pagination
		paginator = Paginator(page_list, 9) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			page_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			page_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			page_list = paginator.page(paginator.num_pages)

		# Fixing the proplem f the reptitave Page attribute in URL
		url_without_page = request.GET.copy()
		if 'page' in url_without_page:
			del url_without_page['page']
		
		# FInal Context Variables to Send
		context = {
			'page_list': page_list,
			'url_without_page':url_without_page,

		}
		return render(request,'product/category_list.html', context)




def product_detail(request, id, slug):
		"""
			For displying All information related to ONE Products and listing all categories
		"""
		#for listing Categories othat has at least one published product
		categories = Category.objects.filter(products__is_published=True).distinct()
		product = get_object_or_404(Product,id=id,slug=slug,is_published=True)
		related_categories = product.categories.all()
		# Related products List has the same category as the current prodcut without repeatition. 
		related_products = Product.objects.filter(categories__in=list(related_categories)).exclude(id=product.id).distinct()
		#intializing the cart form
		cart_product_form = CartAddProductForm()
		# Final Context Variables to Send back
		context = {
			'categories': categories,
			'product': product,
			'related_products':related_products,
			'cart_product_form':cart_product_form
		}
		return render(request,'product/detail.html', context)



def search_product(request):
		"""
		This View will relay on the request context valriables anc check all posibilities/criterias and search the DB
		"""
		#for listing Categories othat has at least one published product
		categories = Category.objects.filter(products__is_published=True).distinct()

		# If this is a GET request then process the Form data
		if request.method == 'GET':
			# Create a form instance and populate it with data from the request (binding):
			form=SearchForm(request.GET)
			# Check if the form is valid:
			if form.is_valid():
				# Maping the Search From to our variables and intialization 
				search_category_object = None
				# Represent the Products
				page_list = None
				total_results = 0
				original_search_text = form.cleaned_data['search_query']
				search_text = original_search_text.strip()
				max_price = form.cleaned_data['max_price']
				search_category_name = form.cleaned_data['search_category']
				is_exact_match = form.cleaned_data['is_exact_match']
				show_count = form.cleaned_data['show_count']
	
				if  search_category_name != "None" and search_category_name != "":
					search_category_object = get_object_or_404(Category, name=search_category_name)
				
				if is_exact_match == False:
					# Replacing Spaces with | to search on each word included separetly 
					search_text = re.sub(r' +',"|",search_text)
				
				# if A SearchText is entered
				if search_text != '' or search_text == None:

					if search_category_object:
						if max_price == None:
							# Do Search based on SearchText + Category
							page_list = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(categories__in=[search_category_object])
						else:
							# Do Search based on SearchText + Category + Max
							page_list = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(categories__in=[search_category_object]).filter(price__lte=max_price)
					else:
						if max_price == None:
							# Do Search based on SearchText only
							page_list = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True)
						else:
							# Do Search based on SearchText + MAX
							page_list = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(price__lte=max_price)
				# if no SearchText is entered
				else:
					if search_category_object:
						if max_price == None:
							# Do Search based on Category only
							page_list = Product.objects.filter(categories__in=[search_category_object],is_published=True)
						else:
							# Do Search based on Category + MAX
							page_list = Product.objects.filter(is_published=True).filter(categories__in=[search_category_object]).filter(price__lte=max_price)
					else:
						if max_price == None:
							# Do Search based on NOTHING Selcted
							start_search='StartSearch'
							context = {'categories': categories,'start_search':start_search}
							return render(request,'product/search.html',context)
						else: 
							# Do Search based on MAX only
							page_list = Product.objects.filter(is_published=True).filter(price__lte=max_price)

				# Getting the number of results
				if page_list == None:
					total_results = 0
				else:
					total_results = page_list.count()
				

				# handeling Paganation & Items count per page
				if show_count:
					paginator = Paginator(page_list, show_count)
				else:
					 paginator = Paginator(page_list, 10)
					 show_count = 10

				page = request.GET.get('page')
				try:
					page_list = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					page_list = paginator.page(1)
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					page_list = paginator.page(paginator.num_pages)

				# Fixing the proplem of the reptitave Page attribute in URL
				url_without_page = request.GET.copy()
				if 'page' in url_without_page:
					del url_without_page['page']

				# Final Context Variables to Send back
				context = {
					'categories': categories,
					'page_list': page_list,
					'category':search_category_object,
					'original_search_text':original_search_text,
					'max_price':max_price,
					'is_exact_match':is_exact_match,
					'total_results':total_results,
					'show_count':show_count,
					'url_without_page':url_without_page,
				}

				return render(request,'product/search.html', context)
			else:
				print ("***************** NOT VALID *********************")
				context = {'categories': categories,}
				return render(request,'product/search.html',context)
		else:
			print ("***************** NOT GET *********************")
			return 
