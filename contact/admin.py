from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

	readonly_fields=(["applied_timestamp"])
	list_display = ("first_name","last_name","email","message_type")
	list_display_links = ("first_name","last_name","email",)
	list_filter = ("applied_timestamp",)

