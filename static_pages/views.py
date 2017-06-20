from django.shortcuts import render

# Create your views here.
def about(request):
	context = locals()
	template = 'static_pages/about.html'
	return render(request,template, context)