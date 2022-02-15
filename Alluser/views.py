from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from . import models
# Create your views here.
def home(request):
    if request.method == 'POST':
        if len(request.POST.get('MobileNo'))==14:
            Mobile_Number = request.POST.get('MobileNo')
            PassWord = request.POST.get('password-field')
            print(Mobile_Number,PassWord)
            try :
                user = authenticate(request,mobile=Mobile_Number,password=PassWord)
                print(user)
                if user is not None :
                    login(request,user)
                    url = '/dashboard/?pk={}'.format(user.id)
                    return HttpResponseRedirect(url)
                else :
                    messages.info(request,"Enter Valid Credentials")
                    return render(request,'login.html')
            except User.DoesNotExist:
                messages.info(request,"User is Not Here")
                return render(request,'login.html')
        else :
            messages.info(request,"Including +91 There should be Valid 10 Digit Mobile No")
            return render(request,'login.html')
    return render(request,'login.html',{'dis':'d-none'})

def signup(request):
    if request.method == 'POST':
        if len(request.POST.get('MobileNo'))==14:
            Mobile_Number = request.POST.get('MobileNo')
            PassWord = request.POST.get('password-field')
            Name =  request.POST.get('Name')
            Email = request.POST.get('Email')
            try :
                user = authenticate(request,mobile=Mobile_Number)
                if user is not None:
                        messages.info(request,"User is Already Here")
                        return render(request,'login.html')
                else :
                    print('else')
                    user = models.User(mobile=Mobile_Number,name=Name,email=Email)
                    user.set_password(PassWord)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    print("Save",user)
                    messages.success(request,"Registration Sucessful")
                    return render(request,'login.html')
            except Exception as err :
                messages.info(request,"Mobile Number Will Be Like This +91 1234567890")
                return render(request,'signup.html')
    return render(request,'signup.html',{'dis':'d-none'})
