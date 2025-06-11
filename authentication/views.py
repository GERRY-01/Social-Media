from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Registration
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        has_error = False
    
        if password != confirm_password:
            messages.error(request, 'Passwords are not matching')
            has_error = True
            
        if User.objects.filter(username = username).exists():
            messages.error(request, "this username is taken")
            has_error = True
            
        if User.objects.filter(email = email).exists():
            messages.error(request, "this email already exists")
            has_error = True
            
        if has_error:
            return redirect("register")
        
        user_data = User.objects.create_user(first_name = first_name,last_name = last_name, username = username, email = email, password=password)
        user_data.save()
        login(request, user_data)
        return redirect("completeregistration")
    return render(request, 'registration.html')

def completeregistration(request):
    if request.method == 'POST':
        user = request.user
        profile = request.FILES.get('profile_picture')
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        location = request.POST.get("location")
        hobbies = request.POST.get("hobbies")
        
        reg_data = Registration(user = user, image = profile, dob = dob, gender = gender, location = location, hobbies = hobbies)
        reg_data.save()
        return redirect("home")
    return render(request, 'completeregistration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'invalid login')
        
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect("login")