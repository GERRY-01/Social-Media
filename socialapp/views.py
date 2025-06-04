from django.shortcuts import get_object_or_404, render,redirect
from . models import Comments, Posts,Likes
from authentication.models import Registration,User
# Create your views here.
def home(request):
    if request.user.is_authenticated: 
        try:
            profile = Registration.objects.get(user = request.user)
        except Registration.DoesNotExist:
            profile = None
            
    else: 
        profile = None
    if request.method == 'POST':
        if 'media' in request.FILES:
            file = request.FILES.get("media")
            caption = request.POST.get("caption")
            my_posts = Posts(user = request.user,media = file, caption = caption)
            my_posts.save()
            return redirect("home")
    
    all_posts = Posts.objects.all().order_by('-id')
    
    for post in all_posts:
         post.is_liked = post.likes.filter(user=request.user).exists()

    
    return render(request, 'home.html', {'all_posts':all_posts,'profile':profile})

def add_comment(request, post_id):
    if request.method == 'POST':
        comment_text = request.POST.get("comment_text")
        post = get_object_or_404(Posts, id=post_id)
        Comments.objects.create(user = request.user,post=post, content=comment_text)
        return redirect("home")

def likes(request, post_id):
    post = get_object_or_404(Posts, id = post_id)
    like, created = Likes.objects.get_or_create(user = request.user, post= post)
    if not created:
        like.delete()
    return redirect("home")

def profile(request):
    user_posts = Posts.objects.filter(user = request.user).order_by('-id')
    return render(request, 'profile.html',{'user_posts':user_posts})