from django.shortcuts import render, redirect,render_to_response,HttpResponse
from .forms import LogForm
from .models import client
import time
import base64
# Create your views here.

def index(request):
    # return render(request,'clientLogin/index.html')#原来的界面
    return render(request, 'clientLogin/clientLogin.html')#改后的界面

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
        ok = client.objects.filter(username=username, password=password).filter()
        if ok:#if exist
            #Generate random Numbers using timestamps
            randomTime=int(time.time())

            #encrypt session
            sessonid=hash(str(randomTime)+username+'myproject')
            sessonid=str(base64.b64encode(str(sessonid).encode('utf-8')),'utf-8')

            #save session
            request.session[sessonid]=username+password

            #set cookies
            response=redirect('/client/home/')
            response.set_signed_cookie('session',sessonid,max_age=60*120,salt='thisProject')
            return response
        return render(request, 'clientLogin/index.html')
    else:
        return render(request,'clientLogin/index.html')


def home(request):
    #get sessionid from cookies
    sessionid=request.get_signed_cookie('session',salt='thisProject')

    is_login=request.session.get(sessionid,False)
    if is_login:    #if have session
        data=request.session.get(sessionid,None)
        print(data)
        return render(request,'clientLogin/success.html')
    else:
        return redirect('/client/index/')

def signOut(request):
    # get sessionid from cookies
    request.session.flush()
    return redirect('/client/index/')

# def test(request):
#     test=client(username='1111',password='2222')
#     test.save()
#     return HttpResponse
