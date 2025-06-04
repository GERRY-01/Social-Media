from django.db import models
from authentication.models import User

# Create your models here.
class Posts(models.Model):
    media = models.FileField(upload_to='files')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','post')