from django.conf.urls import url
from . import views

urlpatterns = [    
		url(r'^search/', views.search_product,name='search_product'),
		url(r'^categories/$', views.category_list,name='category_list'),
		url(r'^(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_by_category'),
		url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
		url(r'^$', views.product_list, name='product_list'),
	]