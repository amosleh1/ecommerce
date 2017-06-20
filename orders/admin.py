from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	fieldsets =[ 
		(None,{"fields":[ 'product','price', 'quantity',]}),
			]
	raw_id_fields = ['product']
	readonly_fields=(  'product','price', 'quantity',)

	def has_add_permission(self, request):
		return False
	def has_delete_permission(self, request, obj=None):
		return False

class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderItemInline]
	list_display = [ 'id','first_name', 'last_name', 'email', 'phone', 'created', 'updated',
					 'country', 'city', 'paid', ]
	list_filter = ['paid', 'created',]
	readonly_fields=( 'email','first_name', 'last_name','phone','address', 'country', 'city','created', 'updated','paid')
	search_fields = ("email", "first_name", "last_name",)

	def has_add_permission(self, request):
		return False
	#Remove the Actions option inside the Admin "Email Address" List
	def get_actions(self, request):
		return
admin.site.register(Order, OrderAdmin)