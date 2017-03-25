from django import forms
	'''
	From for searching a product
	'''
class SearchForm(forms.Form):    
	search_query = forms.CharField(
			label='Search a Product',
			help_text='Type Product Name',
			error_messages{
				'required':'Please Entera Search Text'
			})
	is_exact_match = forms.BooleanField(label='Exact Match',required=False,)
	