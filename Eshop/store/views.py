from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

# Create your views here.
class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:

            quantity = cart.get(product)
            
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1   
        else:
            cart={}
            cart[product] = 1

        request.session['cart'] = cart
       # print('card',request.session['cart'])        
        return redirect('index')


    def get(self, request):

        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        products = None
        
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)
        



    

       
class Signup(View):

    def get(self, request):
        return render(request,'signup.html')


    def post(self, request):
        postdata = request.POST
        first_name = postdata.get('firstname')
        last_name = postdata.get('lastname')
        phone = postdata.get('phone')
        email = postdata.get('email')
        password = postdata.get('password')
    # send value to server
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        customer = Customer(first_name=first_name, last_name=last_name,
                         phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
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
            error_message = "First_name required"

        elif len(customer.first_name) < 4:
            error_message = "first_name should be 4 character"

        elif (not customer.last_name):
            error_message = "Last_name required"

        elif len(customer.first_name) < 4:
            error_message = "last_name should be 4 character"

        elif not customer.phone:
            error_message = "phone required"

        elif len(customer.phone) < 10:
            error_message = "phone number must be 10 char long"

        elif len(customer.password) < 6:
            error_message = "password must be 6 char long"

        elif len(customer.email) < 6:
            error_message = "emailmust be 10 char long"
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message
    


class Login(View):
    def get(self, request):
        return render(request,'login.html')   
        
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                #request.session['email'] = customer.email
                return redirect('index')
            else:
                error_message = 'email or password invalid'

        else:
            error_message = 'email or password invalid'

        return render(request,'login.html',{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        return render(request, 'cart.html', {'products': products})

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(address,phone,customer,cart,products)
        for product in products:
            order = Order( customer = Customer(id = customer),
                           product = product,
                           price = product.price,
                           address = address,
                           phone = phone,
                           quantity = cart.get(str(product.id)))
            order.placeOrder()            
        request.session['cart'] = {}       
        return redirect('cart')

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        
        return render(request, 'orders.html', {'orders': orders})


        