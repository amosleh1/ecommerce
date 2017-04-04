from django import forms

from django.forms import ModelForm
from .models import Career
'''
From for searching a product
'''
class SearchForm(forms.Form):    
	search_query = forms.CharField(
			label='Search a Product',
			help_text='Type Product Name',
			required=False,
	)
	is_exact_match = forms.BooleanField(label='Exact Match',required=False)
	max_price = forms.DecimalField(max_digits=10, decimal_places=2 ,required=False)
	search_category = forms.CharField(required=False)


class CareerForm(ModelForm): 
	class Meta:
		model = Career