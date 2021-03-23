from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages 
from django.core.mail import send_mail


# Create your views here.



def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)   
            return redirect('userpage')
        else:
            messages.info(request, 'invalid username and password')
            return redirect('login')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST['password']
       
        
        

        if User.objects.filter(username = username).exists():
            messages.info(request, 'username already taken..')
            return redirect('signup')
               
        elif User.objects.filter(email = email).exists():
            messages.info(request, 'Email already taken ..')
                
            return redirect('signup')

        else: 
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.info(request, 'User Created Successfully Please Login')
            print('user created')
            return redirect('/')

       
       
        return redirect('/')

    else:        
        return render(request,'signupPage.html')  


       
       

def userpage(request): 
    if request.user.is_authenticated:
        return render(request,'userPage.html')
    else:
        return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('/')   


def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)   
            return redirect('userpage')
        else:
            messages.info(request, 'invalid username and password')
            return redirect('log')
    else:
        return render(request, 'index.html')
