from django.conf.urls import url
from . import views

urlpatterns = [ 
		url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/new_resume/$',views.new_resume,name='new_resume'),   
		url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.vacancy_detail,name='vacancy_detail'),
		url(r'^$', views.vacancy_list,name='vacancy_list'),
	]