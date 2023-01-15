from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .forms import Userform 



# Create your views here.

# class UserData(forms.Form):

def index(request):
    
  if not request.user.is_authenticated:
    print("hee")
    return HttpResponseRedirect(reverse("login"))
  else:
    print(request.user)
    return HttpResponseRedirect(reverse("home"))

def register(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("home"))
  else:
    print("yewruklq")
    if request.method=="POST":
      form=Userform(request.POST)
      if form.is_valid():
        
        form.save()
        print("dfjdsf")
        return HttpResponseRedirect(reverse("login"))

      else:
        return render(request,'register.html',{
          "form":form
        })
    else:
      print("jhdsfjshkdf")
      form=Userform()
      return render(request,'register.html',{
        "form":form
      })

  

def login_view(request):
  # request.session['message']="NULL"
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("home"))
  else:
    if request.method=="POST":
      username=request.POST["username"]
      password=request.POST["password"]

      user=authenticate(request,username=username,password=password)
      if user is not None:
        login(request,user)
        request.session['userId'] = user.id
        return HttpResponseRedirect(reverse("home"))
      else:
        return HttpResponseRedirect(reverse('login'))
    
    return render(request,'login.html')

def logout_view(request):
  logout(request)
  if request.session.get('userId'):
    del request.session['userId']
  return HttpResponseRedirect(reverse('login'))