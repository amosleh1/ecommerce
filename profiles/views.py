
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


	

@login_required
def profile_view_update(request):
	"""
		Update profile information
	"""
	message = ''
	# Get the context from the request
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form=UserProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			userProfile = form.save(commit=False)
			userProfile.email = form.cleaned_data['email']
			userProfile.phone = form.cleaned_data['phone']
			userProfile.gender = form.cleaned_data['gender']
			userProfile.nationality = form.cleaned_data['nationality']
			userProfile.first_name = form.cleaned_data['first_name']
			userProfile.last_name = form.cleaned_data['last_name']
			userProfile.save()
			context = {
				'message':"Your Message has been Submitted Successfully", 
				'form': form,
			}
			'''
			# Handeling Email attributes and sending one
			#user_message = form.cleaned_data['message']
			#user_firstName = form.cleaned_data['first_name']
			#user_email = form.cleaned_data['email']
			#email_subject = 'My ECommerce - New Contact Submitted'
			#email_message = '%s %s' %(user_message, user_firstName)
			#email_from = user_email 
			#email_to = [settings.EMAIL_HOST_USER]
			#send_mail(email_subject,email_message,email_from, email_to, fail_silently=True)
			'''
			return render(request, "profiles/profile.html", context)
		else:
			print (form.errors)	
			message = form.errors

	else:
		# Not a POST so Generate New Empty Form from UserProfile from the Instance we have
		form = UserProfileForm(instance=request.user)

	context = {
		'form': form,
		'message': message,
	}
	return render(request, "profiles/profile.html", context)
