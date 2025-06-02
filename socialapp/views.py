from django.shortcuts import render,redirect
from . models import Posts
# Create your views here.
def home(request):
    if request.method == 'POST':
        file = request.FILES.get("media")
        caption = request.POST.get("caption")
        my_posts = Posts(media = file, caption = caption)
        my_posts.save()
        return redirect("home")
    
    all_posts = Posts.objects.all().order_by('-id')
    return render(request, 'home.html', {'all_posts':all_posts})