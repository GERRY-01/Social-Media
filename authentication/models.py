from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics')
    dob = models.DateField()
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),   
    ]
    
    gender = models.CharField(choices=gender_choices, max_length=10)
    location = models.CharField(max_length=50)
    hobbies = models.CharField(max_length=200)