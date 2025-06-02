from django.db import models

# Create your models here.
class Posts(models.Model):
    media = models.FileField(upload_to='files')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)