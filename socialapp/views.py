from django.shortcuts import get_object_or_404, render,redirect
from . models import Comments, Posts,Likes,Follow
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
    suggestions = User.objects.exclude(id = request.user.id)[:5] if request.user.is_authenticated else []
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)) if request.user.is_authenticated else set()
    
    
    for post in all_posts:
         post.is_liked = post.likes.filter(user=request.user).exists()

    
    return render(request, 'home.html', {'all_posts':all_posts,'profile':profile,'suggestions':suggestions,'following_ids':following_ids})

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
    followers = Follow.objects.filter(following = request.user).count()
    following = Follow.objects.filter(follower = request.user).count()
    posts_count = user_posts.count()

    return render(request, 'profile.html',{'user_posts':user_posts,'followers':followers,'following':following,'posts_count':posts_count})

def follow(request, user_id):
    target_user = get_object_or_404(User, id = user_id)
    
    if request.user == target_user:
        return redirect("home")
    
    follow, created = Follow.objects.get_or_create(follower = request.user, following = target_user)
    if not created:
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def view_profile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    user_posts = Posts.objects.filter(user = user).order_by('-id')
    real_followers = Follow.objects.filter(following = user)
    real_following = Follow.objects.filter(follower = user)
    followers = Follow.objects.filter(following = user).count()
    following = Follow.objects.filter(follower = user).count()
    posts_count = user_posts.count()
    is_following = Follow.objects.filter(follower = request.user, following = user).exists()
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'view_profile.html',{'user':user,'user_posts':user_posts,'followers':followers,'following':following,'posts_count':posts_count,'is_following':is_following,'following_ids':following_ids, 'real_followers':real_followers,'real_following':real_following})

    
def error_404(request, exception):
    return render(request, '404.html', status=404)