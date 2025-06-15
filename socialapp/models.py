from django.db import models
from authentication.models import User
from django.utils import timezone

# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='posts')
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
        
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete= models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower','following')
        
class Stories(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='files')
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(default=lambda:timezone.now() + timezone.timedelta(days=1))
    
    class Meta:
        ordering = ['-created_at']