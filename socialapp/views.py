from django.shortcuts import get_object_or_404, render,redirect
from . models import Comments, Posts
# Create your views here.
def home(request):
    if request.method == 'POST':
        if 'media' in request.FILES:
            file = request.FILES.get("media")
            caption = request.POST.get("caption")
            my_posts = Posts(media = file, caption = caption)
            my_posts.save()
            return redirect("home")
    
    all_posts = Posts.objects.all().order_by('-id')
    return render(request, 'home.html', {'all_posts':all_posts})

def add_comment(request, post_id):
    if request.method == 'POST':
        comment_text = request.POST.get("comment_text")
        post = get_object_or_404(Posts, id=post_id)
        Comments.objects.create(post=post, content=comment_text)
        return redirect("home")
