from django.conf.urls import url
from . import views

urlpatterns = [
		#url(r'^update/(?P<id>\d+)/',views.update, name='profile_update'),
		url(r'^$', views.profile_view_update, name='profile_view_update'),
	]