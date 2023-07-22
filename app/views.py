from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from app.forms import *
# Create your views here.
def registration(request):
    USFO=UserForm()#user_form_object
    PFO=ProfileForm()#profile_form_object
    d={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        #when we are dealing with both data and files(images)
        USFD=UserForm(request.POST)
        #Formobject returned with some data that we are collecting and storing in USFD
        PFD=ProfileForm(request.POST,request.FILES)
        #profile form is dealing with both data and files
        if USFD.is_valid() and PFD.is_valid():
            NSUFO=USFD.save(commit=False)#by default it will be true
            #it will return a not saved userform object
            submitpwd=USFD.cleaned_data['password']
            #collecting data i.e., user submitted password
            NSUFO.set_password(submitpwd)
            #performing encrypt password operation by using set_password method
            NSUFO.save()
            NSPFO=PFD.save(commit=False)
            #want to add a username column for that we are providing an object as value
            NSPFO.username=NSUFO
            NSPFO.save()
            send_mail('Registration','Registration is successfull check in admin',
                      'madhunarayana2603@gmail.com',[NSUFO.email],fail_silently=False)
            return HttpResponse('Registration is successfull')
        else:
            return HttpResponse('try again')

    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')#collecting username of login user 
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        #authenticate is a function to check for authentication(checking) and authorization(allowing permission)
        if AUO:
            if AUO.is_active:#checking whether the user is active or not
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))









