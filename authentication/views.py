from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .forms import Userform 





def index(request):
  if not request.user.is_authenticated:
    return HttpResponseRedirect(reverse("login"))
  else:
    return HttpResponseRedirect(reverse("home"))

def register(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("home"))
  else:
    if request.method=="POST":
      form=Userform(request.POST)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("login"))

      else:
        return render(request,'register.html',{
          "form":form
        })
    else:
      form=Userform()
      return render(request,'register.html',{
        "form":form
      })

  

def login_view(request):
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