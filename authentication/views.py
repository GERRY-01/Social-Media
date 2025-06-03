from django.shortcuts import render,redirect
from django.contrib.auth.models import User
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
        
        user_data = User(first_name = first_name,last_name = last_name, username = username, email = email, password=password)
        user_data.save()
        return redirect("completeregistration")
    return render(request, 'registration.html')