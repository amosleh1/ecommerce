from django.shortcuts import render, get_object_or_404
# used for pagnation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#used for my customized created models
from .models import Vacancy, Resume

from .forms import ResumeForm
from django.http import HttpResponse

def vacancy_list(request):
		"""
			For displying All vacancies
		"""
		#for listing Categories on the lift side of the page
		vacancies = Vacancy.objects.filter(is_published=True)

		# Pagination
		paginator = Paginator(vacancies, 5) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			vacancies = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			vacancies = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			vacancies = paginator.page(paginator.num_pages)

		# Fixing the proplem f the reptitave Page attribute in URL
		url_without_page = request.GET.copy()
		if 'page' in url_without_page:
			del url_without_page['page']

		# FInal Context Variables to Send
		context = {
			'vacancies': vacancies,
			'url_without_page':url_without_page,
		}
		return render(request,'career/vacancy_list.html', context)



def vacancy_detail(request, id, slug):
		"""
			For displying All information related to ONE vacancy
		"""
		vacancy = get_object_or_404(Vacancy,id=id,slug=slug,is_published=True)

		# Final Context Variables to Send back
		context = {
			'vacancy': vacancy,
		}
		return render(request,'career/vacancy_detail.html', context)



def new_resume(request, id, slug):
		"""
			Submit a new resume to an exiting Vacancy
		"""
		vacancy =  get_object_or_404(Vacancy,id=id,is_published=True)
		# Get the context from the request
		resume = None
		if request.method == 'POST':
			# Create a form instance and populate it with data from the request (binding):
			form=ResumeForm(request.POST, request.FILES)
			if form.is_valid():
				#check if the same email used for the same vacancy before
				resume = Resume.objects.filter(email=form.cleaned_data['email']).filter(vacancy= vacancy)
				if not resume:
					resume = form.save(commit=False)
					resume.vacancy = vacancy
					resume.first_name = form.cleaned_data['first_name']
					resume.middle_name = form.cleaned_data['middle_name']
					resume.last_name = form.cleaned_data['last_name']
					resume.nationality = form.cleaned_data['nationality']
					resume.birth_date = form.cleaned_data['birth_date']
					resume.phone = form.cleaned_data['phone']
					resume.email = form.cleaned_data['email']
					resume.comment = form.cleaned_data['comment']
					resume.resume_file = form.cleaned_data['resume_file']
					resume.save()
					context = {
						'message':"You Resume has Been submitted", 
					}
					return render(request, "career/resume_status.html", context)
				else:
					context = {
						'message':"A resume from this email is already subitted to this Vacancy", 
					}
					return render(request, "career/resume_status.html", context)
		else:
			# Not a POST so Generate New Empty Form from Resume Class
			form = ResumeForm()

		context = {
			'form': form,
			'vacancy':vacancy,
		}
		return render(request, "career/new_resume.html", context)