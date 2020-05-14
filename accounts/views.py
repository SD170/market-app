from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from .models import *

from .decorators import unauthenticated_user,allowed_users,admin_only

from .forms import OrderForm,CustomerForm


from .filters import OrderFilter



@unauthenticated_user
def register(request):

	registration_form = RegisterUserForm()

	if request.method == "POST":
		registration_form = RegisterUserForm(request.POST)
		if registration_form.is_valid():
			registration_form.save()
			
			username = registration_form.cleaned_data.get('username')

			messages.success(request, username + ' Has successfully registerd')
			return redirect ('login')
			
	context={'registration_form' : registration_form}

	return render(request, 'accounts/register.html', context)





@unauthenticated_user
def loginpage(request):


	username = request.POST.get('username')
	password = request.POST.get('password')

	user = authenticate(request, username=username, password = password)

	if user is not None:
		login(request,user)
		return redirect('home')
	else:
		messages.info(request,'Username or Password not correct')

	context={}
	return render(request, 'accounts/login.html', context)


def logoutpage(request):
	logout(request)
	return redirect('login')



@login_required(login_url = 'login')
@admin_only
def home(request):

	total_orders = Order.objects.count()
	orders_delivered = Order.objects.filter(status='Delivered').count()
	orders_pending = Order.objects.filter(status='Pending').count()
	conetnts = {
		'models_orders':Order.objects.all(),
		'models_customers':Customer.objects.all(),
		'total_orders':total_orders,
		'orders_delivered':orders_delivered,
		'orders_pending':orders_pending,	
	}


	return render(request, 'accounts/dashboard.html', conetnts)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def userPage(request):
	user_orders = request.user.customer.order_set.all()
	total_orders = user_orders.count()
	orders_delivered = user_orders.filter(status='Delivered').count()
	orders_pending = user_orders.filter(status='Pending').count()

	context={'orders' : user_orders,
			'total_orders':total_orders,
			'orders_delivered':orders_delivered,
			'orders_pending':orders_pending,	
			}
	return render(request, 'accounts/user.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def accountsSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {
				'form' : form,
			}
	return render (request, 'accounts/accounts_settings.html', context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def products(request):

	return render(request, 'accounts/products.html',{'models_products' : Product.objects.all()})


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def customer(request,pk):
	model_customer= Customer.objects.get(id=pk)
	exactly_this_customers_orders = model_customer.order_set.all()

	total_orders = exactly_this_customers_orders.count()

	myfilter = OrderFilter(request.GET, queryset = exactly_this_customers_orders)
	orders = myfilter.qs
	context = {
		'model_customer' : model_customer,
		'orders' : orders,
		'total_orders' : total_orders,
		'myfilter' : myfilter,
	}
	return render(request, 'accounts/customer.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def createOrder(request,pk):

	OrderFormSet = inlineformset_factory(Customer, Order, fields= ('product','status'), extra=5)

	this_customer = Customer.objects.get(id = pk)
	formset = OrderFormSet(queryset = Order.objects.none(), instance = this_customer)


	if request.method =='POST':
		formset = OrderFormSet(request.POST,instance = this_customer)
		if formset.is_valid():
			formset.save()
			return redirect ('/')


	context={
			'formset' : formset,
			'this_customer' : this_customer,
			}

	return render(request,'accounts/createOrder.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def updateOrder (request,pk):
	this_order = Order.objects.get(id=pk)
	form = OrderForm(instance=this_order)

	if request.method == 'POST':
		form=OrderForm(request.POST,instance = this_order)
		if form.is_valid():
			form.save()
			return redirect('/')



	context = {
				'form':form,
				'this_customer':this_order.customer
			}

	return render(request,'accounts/createOrder.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def deleteOrder(request,pk):

	this_order = Order.objects.get(id=pk)
	context = {'product' : this_order.product.name}

	if request.method == 'POST':
		this_order.delete()
		return redirect ('/')

	return render(request,'accounts/deleteOrder.html',context)