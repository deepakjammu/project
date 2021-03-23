from django.shortcuts import render, redirect
from .models import Customer, Product, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm,LoginForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        totalitem = None
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        print(mobiles)
        return render(request, 'home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles,'totalitem':totalitem})

# def product_detail(request):
#     return render(request, 'productdetail.html')


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user=request.user)).exists()

        return render(request, 'productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem} )

@login_required
def add_to_cart(request):
    if request.user.is_authenticated:

        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        # print(product_id)
        return redirect('/cart')
    else:
        return redirect('/accounts/login')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        totalitem = len(Cart.objects.filter(user = request.user))
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
              

            return render(request, 'addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount,'totalitem':totalitem})
        else:
            return render(request, 'emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
       
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
            

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
       
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
                      

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
           
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':

        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
       
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
                  

        data = {
           
            'amount': amount,
            'totalamount': amount + shipping_amount
           
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'buynow.html')

# @login_required
# def profile(request):
#     return render(request, 'profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'orders.html',{'order':op})

# def change_password(request):
#     return render(request, 'changepassword.html')

@login_required
def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'OnePlus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)

    return render(request, 'mobile.html', {'mobiles': mobiles})


# def login(request):
#     return render(request, 'login.html')


class Customerregistration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Congratulations !! Registered Successfully')
        return render(request, 'customerregistration.html', {'form': form})

# def customerregistration(request):
#     return render(request, 'customerregistration.html')

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount =0.0
    shipping_amount = 70.0
    totalamount = 0.0
    
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount +=tempamount
        totalamount = amount +shipping_amount  
        finalamount = (totalamount//shipping_amount)  
    return render(request, 'checkout.html',{'add':add, 'totalamount':totalamount,'cart_items':cart_items,'finalamount':finalamount})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')    

@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):

        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations !! Profile Updated Successfully')

        return render(request, 'profile.html', {'form': form, 'active': 'btn-primary'})

# def logout_view(request):

#     logout(request)
#     return redirect('login')

# def login(request):
#     form = LoginForm()
#     return render(request, 'login.html',{"form":form})