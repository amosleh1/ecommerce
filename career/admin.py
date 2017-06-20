from django.contrib import admin
from .models import Vacancy, Resume


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
	fieldsets =[
		("Vacancy Main Info",{"fields":["title","job_summary","location"]}),
		("Vacancy Details",{"fields":["responsibilities","requirements"]}),
		("Vacancy Controls",{"fields":["is_published",]}),
	]
	readonly_fields=(["created_timestamp"])
	list_display = ("title","location","is_published","created_timestamp")
	list_editable = ("is_published",)
	list_display_links = ("title",)
	list_filter = ("is_published",)
	search_fields = ("title","location")





@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

	readonly_fields=(["applied_timestamp"])
	list_display = ("vacancy","first_name","last_name","nationality","resume_file")
	list_display_links = ("first_name",)
	list_filter = ("vacancy",)
