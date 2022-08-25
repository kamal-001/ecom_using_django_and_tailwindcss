from unicodedata import category
from django.shortcuts import render, redirect, HttpResponseRedirect
from home.models import Customer, Order, Product, Category
from django.views import View
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password

# Create your views here.
class index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('index')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)

# def index(request):
#     return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
    
def product(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'product.html', data)

def productPage(request):
        # cart = request.session.get('cart')
    # if not cart:
        # request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    # print('you are : ', request.session.get('email'))
    return render(request, 'productPage.html', data)

def search(request):
    return render(request, 'search.html')

def faq(request):
    return render(request, 'faq.html')


class signup (View):
	def get(self, request):
		return render(request, 'signup.html')

	def post(self, request):
		postData = request.POST
		first_name = postData.get('firstname')
		last_name = postData.get('lastname')
		phone = postData.get('phone')
		email = postData.get('email')
		password = postData.get('password')
		# validation
		value = {
			'first_name': first_name,
			'last_name': last_name,
			'phone': phone,
			'email': email
		}
		error_message = None

		customer = Customer(first_name=first_name,
							last_name=last_name,
							phone=phone,
							email=email,
							password=password)
		error_message = self.validateCustomer(customer)

		if not error_message:
			print(first_name, last_name, phone, email, password)
			customer.password = make_password(customer.password)
			customer.register()
			return redirect('index')
		else:
			data = {
				'error': error_message,
				'values': value
			}
			return render(request, 'signup.html', data)

	def validateCustomer(self, customer):
		error_message = None
		if (not customer.first_name):
			error_message = "Please Enter your First Name !!"
		elif len(customer.first_name) < 3:
			error_message = 'First Name must be 3 char long or more'
		elif not customer.last_name:
			error_message = 'Please Enter your Last Name'
		elif len(customer.last_name) < 3:
			error_message = 'Last Name must be 3 char long or more'
		elif not customer.phone:
			error_message = 'Enter your Phone Number'
		elif len(customer.phone) < 10:
			error_message = 'Phone Number must be 10 char Long'
		elif len(customer.password) < 5:
			error_message = 'Password must be 5 char long'
		elif len(customer.email) < 5:
			error_message = 'Email must be 5 char long'
		elif customer.isExists():
			error_message = 'Email Address Already Registered..'
		# saving

		return error_message

# def signup (request):
#     return render (request, 'signup.html')

class login(View):
    return_url = None

    def get(self, request):
        login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if login.return_url:
                    return HttpResponseRedirect (login.return_url)
                else:
                    login.return_url = None
                    return redirect ('index')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

# def login (request):
#     return render (request, 'login.html')

# def logout (request):
#     return render (request, 'logout.html')

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request , 'cart.html' , {'products' : products} )

# class checkOut(View):
#     def post(self, request):
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         customer = request.session.get('customer')
#         cart = request.session.get('cart')
#         products = Product.get_products_by_id(list(cart.keys()))
#         print(address, phone, customer, cart, products)

#         for product in products:
#             print(cart.get(str(product.id)))
#             order = Order(customer=Customer(id=customer),
#                           product=product,
#                           price=product.price,
#                           address=address,
#                           phone=phone,
#                           quantity=cart.get(str(product.id)))
#             order.save()
#         request.session['cart'] = {}

#         return redirect('cart')

class checkOut(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request , 'checkout.html' , {'products' : products} )
	
def orders (request):
    return render (request, 'orders.html')