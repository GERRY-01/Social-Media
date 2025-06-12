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
    
class Room(models.Model):
    name = models.CharField(max_length=1000)
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    