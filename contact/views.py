from django.shortcuts import render, get_object_or_404
#used for my customized created models
from .models import Contact
from .forms import ContactForm
#used for sending emails
from django.core.mail import send_mail
from django.conf import settings


def new_message(request):
		"""
			Submit a new contact Message to DB
		"""
		# Get the context from the request
		if request.method == 'POST':
			# Create a form instance and populate it with data from the request (binding):
			form=ContactForm(request.POST)
			if form.is_valid():

					contact = form.save(commit=False)
					contact.first_name = form.cleaned_data['first_name']
					contact.middle_name = form.cleaned_data['middle_name']
					contact.last_name = form.cleaned_data['last_name']
					contact.phone = form.cleaned_data['phone']
					contact.email = form.cleaned_data['email']
					contact.message = form.cleaned_data['message']
					contact.message_type = form.cleaned_data['message_type']
					contact.save()
					context = {
						'message':"Your Message has been Submitted Successfully", 
					}

					# Handeling Email attributes and sending one
					contact_message = form.cleaned_data['message']
					contact_firstName = form.cleaned_data['first_name']
					contact_email = form.cleaned_data['email']
					email_subject = 'My ECommerce - New Contact Submitted'
					email_message = '%s %s' %(contact_message, contact_firstName)
					email_from = contact_email 
					email_to = [settings.EMAIL_HOST_USER]
					send_mail(email_subject,email_message,email_from, email_to, fail_silently=True)

					return render(request, "contact/contact_status.html", context)	
		else:
			# Not a POST so Generate New Empty Form from Contact Class
			form = ContactForm()

		context = {
			'form': form,
		}
		return render(request, "contact/contact.html", context)