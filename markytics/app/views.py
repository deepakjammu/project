from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.models import User,auth
from .models import Report

# Create your views here.
def home(request):
    return render(request,'index.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)  
            messages.info(request, 'Success: You are now logged in.') 
            return redirect('home')

        else:
            messages.info(request, 'User does not exist!!')
            return redirect('login')
   
    else:
        return render(request,'login.html')    


def report(request):
    if request.method == 'POST':
        incident_department = request.POST['incident_department']
        description = request.POST.get('description')
        date  = request.POST['date']
        time = request.POST['time']
        incident_location = request.POST['incident_location']
        severity = request.POST['severity']
        cause = request.POST['cause']
        type_env  = request.POST.get('type_env')
        type_inju  = request.POST.get('type_inju')
        type_property = request.POST.get('type_property')
        type_vehicle = request.POST.get('type_vehicle')
        reportedby_id = request.POST.get('reportedby_id')
        report = Report.objects.create(incident_department=incident_department,description=description, date=date,time=time, incident_location= incident_location, severity= severity,cause=cause, type_env= type_env,type_inju=type_inju,type_property=type_property,type_vehicle=type_vehicle, reportedby_id=reportedby_id)
        report.save()
        messages.info(request, 'Report Created Successfully ..')
        return redirect('home')
   
    

    return render(request,'report.html')    


def register(request):
   
    if request.method == 'POST':
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        email= request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'username already taken..')
               
                return redirect('register')

            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email already taken ..')
                
                return redirect('register')

            else: 
                user = User.objects.create_user(username=username,email=email, password=password1)
                user.save()
                messages.info(request, 'User Created Successfully ..')
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Password is not matching ..')
            print('password not matching')
            return redirect('register')
    
    else:
        return render(request,'register.html')



def logout(request):
    auth.logout(request)
    return redirect('home')         
