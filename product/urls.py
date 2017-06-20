from django.conf.urls import url
from . import views

urlpatterns = [    
		url(r'^search', views.search_product,name='search'),
		url(r'^categories', views.category_list,name='categories'),
		url(r'^promotion', views.promotion_list,name='promotion_list'),
		url(r'^(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_by_category'),
		url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
		url(r'^$', views.product_list, name='product_list'),
	]