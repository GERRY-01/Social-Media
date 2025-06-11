from django.urls import path
from . import views
urlpatterns = [
    path("/register",views.register,name="register"),
    path("/register/complete_registration",views.completeregistration,name="completeregistration"),
    path("/login", views.user_login, name="login"),
    path("/logout", views.user_logout, name="logout"),
    
]
