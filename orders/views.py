from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required



@login_required
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			'''
			It is advisable to handle empty cart with orders that is 0 cost
			'''
			order = form.save(commit=False)
			order.user = request.user
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])  
			# clear the cart
			cart.clear()
			return render(request, 'orders/order_detail.html', {'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'orders/order_detail.html', {'cart': cart, 'form': form})