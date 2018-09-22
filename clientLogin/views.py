from django.shortcuts import render, redirect,render_to_response,HttpResponse
from .forms import LogForm
from .models import client
import time
import base64
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def toBase(request):
    return render(request,"clientLogin/base.html")


def index(request):
    #get sessionid from cookies
    sessionid=""
    try:
        sessionid=request.get_signed_cookie('session',salt='thisProject')
    except Exception as e:
        pass
    is_login=request.session.get(sessionid,False)
    if is_login:    #if have session
        data=request.session.get(sessionid,None)

        return render(request,'clientLogin/loginOk.html')
    else:
        return render(request, 'clientLogin/index.html')




def login(request):
    if request.method=='POST':
        username=''
        password=''
        form = LogForm(request.POST)
        if form.is_valid():
            #get the data in the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        #Determine if the user exists
        ok1 = client.objects.filter(username=username, password=password).filter()
        ok2=client.objects.filter(email=username,password=password).filter()
        if (ok1 or ok2):#if exist
            #Generate random Numbers using timestamps
            randomTime=int(time.time())

            #encrypt session
            sessonid=hash(str(randomTime)+username+'myproject')
            sessonid=str(base64.b64encode(str(sessonid).encode('utf-8')),'utf-8')

            #save session
            request.session[sessonid]=username+password

            #set cookies
            response=redirect('/login/home/')
            response.set_signed_cookie('session',sessonid,max_age=60*120,salt='thisProject')
            return response
        return render(request, 'clientLogin/index.html',{'loginError':'Invalid Username or Password'})
    else:
        return render(request,'clientLogin/index.html',{'loginError':'Invalid Username or Password'})


def home(request):
    #get sessionid from cookies
    sessionid=request.get_signed_cookie('session',salt='thisProject')

    is_login=request.session.get(sessionid,False)
    if is_login:    #if have session
        data=request.session.get(sessionid,None)
        print(data)
        return render(request,'clientLogin/loginOk.html')
    else:
        return redirect('/login/index/')

def signOut(request):
    # get sessionid from cookies
    request.session.flush()
    return redirect('/login/index')






