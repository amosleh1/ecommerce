from django.shortcuts import render, get_object_or_404
# used for pagnation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#used for my customized created models
from .models import Category, Product

from .forms import SearchForm
#used for normalizing my search text
import re






def product_list(request, category_slug=None):
		"""
			For displying All products and Categories
		"""
		#for listing Categories on the lift side of the page
		categories = Category.objects.all()

		category = None
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
		return render(request,'product/product_list.html', context)


def category_list(request):
		"""
			For displying All Categories
		"""
		categories = Category.objects.all()

		# Pagination
		paginator = Paginator(categories, 8) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			categories = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			categories = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			categories = paginator.page(paginator.num_pages)
		# FInal Context Variables to Send
		context = {
			'categories': categories,
		}
		return render(request,'product/category_list.html', context)




def product_detail(request, id, slug):
		"""
			For displying All information related to ONE Products and listing all categories
		"""
		#for listing Categories on the lift side of the page
		categories = Category.objects.all()

		product = get_object_or_404(Product,id=id,slug=slug,is_published=True)
		related_categories = product.categories.all()
		# Related products List has the same category as the current prodcut without repeatition. 
		related_products = Product.objects.filter(categories__in=list(related_categories)).exclude(id=product.id).distinct()
		
		# Final Context Variables to Send back
		context = {
			'categories': categories,
			'product': product,
			'related_products':related_products
		}
		return render(request,'product/detail.html', context)



def search_product(request):
		"""
		This View will relay on the request context valriables anc check all posibilities/criterias and search the DB
		"""
		#for listing Categories on the lift side of the page
		categories = Category.objects.all()

		# If this is a GET request then process the Form data
		if request.method == 'GET':
			# Create a form instance and populate it with data from the request (binding):
			form=SearchForm(request.GET)
			# Check if the form is valid:
			if form.is_valid():
				# Maping the Search From to our variables and intialization 
				search_category_object = None
				products = None
				total_results = 0
				original_search_text = form.cleaned_data['search_query']
				search_text = original_search_text.strip()
				max_price = form.cleaned_data['max_price']
				search_category_name = form.cleaned_data['search_category']
				is_exact_match = form.cleaned_data['is_exact_match']
	
				print("******************  HI 3.5 --> max price = ",max_price,"  is Exact = ",is_exact_match," Category Name",search_category_name," ***********************")
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
							products = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(categories__in=[search_category_object])
						else:
							# Do Search based on SearchText + Category + Max
							products = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(categories__in=[search_category_object]).filter(price__lte=max_price)
					else:
						if max_price == None:
							# Do Search based on SearchText only
							products = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True)
						else:
							# Do Search based on SearchText + MAX
							products = Product.objects.filter(name__iregex=r'('+search_text+r')').filter(is_published=True).filter(price__lte=max_price)

				# if no SearchText is entered
				else:
					if search_category_object:
						if max_price == None:
							# Do Search based on Category only
							products = Product.objects.filter(categories__in=[search_category_object],is_published=True)
						else:
							# Do Search based on Category + MAX
							products = Product.objects.filter(is_published=True).filter(categories__in=[search_category_object]).filter(price__lte=max_price)
					else:
						if max_price == None:
							# Do Search based on NOTHING Selcted
							start_search='StartSearch'
							context = {'categories': categories,'start_search':start_search}
							return render(request,'product/search.html',context)
						else: 
							# Do Search based on MAX only
							products = Product.objects.filter(is_published=True).filter(price__lte=max_price)

				# Getting the number of results
				if products == None:
					total_results = 0
				else:
					total_results = products.count()
				print("******************  HI 6 ***********************")
				
				# handeling Paganation
				paginator = Paginator(products, 3) 
				page = request.GET.get('page')
				try:
					products = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					products = paginator.page(1)
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					products = paginator.page(paginator.num_pages)
				

				# Final Context Variables to Send back
				context = {
					'categories': categories,
					'products': products,
					'category':search_category_object,
					'original_search_text':original_search_text,
					'max_price':max_price,
					'is_exact_match':is_exact_match,
					'total_results':total_results,
					#'form':form
				}


				return render(request,'product/search.html', context)
			else:
				print ("***************** NOT VALID *********************")
				context = {'categories': categories,}
				return render(request,'product/search.html',context)
		else:
			print ("***************** NOT GET *********************")
			return 
