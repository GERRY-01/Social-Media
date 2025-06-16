from datetime import timedelta
from django.db import models
from authentication.models import User
from django.utils import timezone
from django.utils.timezone import localtime

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
   
   
def get_expiry_time():
    return timezone.now() + timezone.timedelta(days=1)

class Stories(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='files')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(default=get_expiry_time)
    
    class Meta:
        ordering = ['-created_at']
        
     #defined this function to format the time of the story   
    def format_story_time(story):
        time_diff = timezone.now() - story.created_at
        if time_diff < timedelta(minutes=1):
            return "Just now"
        elif time_diff < timedelta(hours=1):
            minutes = int(time_diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_diff < timedelta(days=1) and localtime(story.created_at).date() == timezone.now().date():
            return f"Today at {localtime(story.created_at).strftime('%I:%M %p')}"
        else:
            return f"Yesterday at {localtime(story.created_at).strftime('%I:%M %p')}"
