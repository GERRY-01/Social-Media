from django.urls import path
from . import views
urlpatterns = [
    path("/register",views.register,name="register"),
    path("/register/complete_registration",views.completeregistration,name="completeregistration"),
    
]
