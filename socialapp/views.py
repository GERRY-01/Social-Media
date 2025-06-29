from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from . models import Comments, Posts,Likes,Follow,Stories
from authentication.models import Message, Registration, Room
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date,timedelta
from django.utils import timezone
from django.core.paginator import Paginator
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
    stories = Stories.objects.filter(expire_at__gt =timezone.now()).order_by('-created_at')
    users_with_active_stories = Stories.objects.filter(expire_at__gt =timezone.now()).values_list('user_id', flat=True).distinct()
    
    #Adding pagination
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        posts = all_posts
        paginator = Paginator(posts, 5)
        
        try:
            page_obj = paginator.page(page)
        except:
            return JsonResponse({'status':'error','message':'Page not found'})
        
        posts_html = render(request, 'post.html', {'page_obj': page_obj}).content.decode('utf-8')
        return JsonResponse({'posts_html': posts_html})
    else:
        posts = all_posts
        paginator = Paginator(posts, 3)
        page_obj = paginator.page(1)
           
        
    
    #grouping stories by users
    user_stories = defaultdict(list)
    for story in stories:
        user_stories[story.user].append(story)
    
    user_stories = dict(user_stories)
    
    
    for post in all_posts:
         post.is_liked = post.likes.filter(user=request.user).exists()

    
    return render(request, 'home.html', {'profile':profile,'suggestions':suggestions,
                'following_ids':following_ids,'stories':stories,'users_with_active_stories':users_with_active_stories,
                'user_stories':user_stories,'page_obj':page_obj})

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
    
    
    if request.method == 'POST':
        if 'media' in request.FILES:
            file = request.FILES.get("media")
            caption = request.POST.get("caption")
            my_story = Stories(user = request.user,media = file, caption = caption)
            my_story.save()
            return redirect("home")
    stories = Stories.objects.filter(expire_at__gt =timezone.now())
    return render(request, 'profile.html',{'user_posts':user_posts,'followers':followers,'following':following,'posts_count':posts_count,'stories':stories})

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


def get_room_name(sender_id, receiver_id):
    sorted_ids = sorted([sender_id, receiver_id])
    return f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

def messages(request):
    other_users = User.objects.exclude(id = request.user.id)
    chat_with = request.GET.get('chat_with')
    selected_user = None
    messages = []
    other_users = User.objects.exclude(id=request.user.id)
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    unread_counts = (
        Message.objects
        .filter(receiver=request.user, is_read=False)
        .values('sender')
        .annotate(count=Count('id'))
    )
    
    
    # Map sender ID to unread count
    unread_map = {item['sender']: item['count'] for item in unread_counts}
           
    
    if chat_with:
        selected_user = get_object_or_404(User, id=int(chat_with))
        room_name = get_room_name(request.user.id, selected_user.id)
        room,_ = Room.objects.get_or_create(name=room_name)
        
          # Mark messages as read
        Message.objects.filter(
            room=room,
            sender=selected_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        messages = Message.objects.filter(room=room).order_by('sent_at')
    return render(request, 'messages.html',{'other_users':other_users,'selected_user':selected_user,'messages':messages,'unread_map':unread_map,'today':today,'yesterday':yesterday})


def view_story(request, story_id):
    selected_story = get_object_or_404(Stories, id = story_id)
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    is_video = any(selected_story.media.name.endswith(ext) for ext in video_extensions)
    user = selected_story.user
    user_stories = Stories.objects.filter(user = user,expire_at__gt =timezone.now()).order_by('-created_at')
    return render(request, 'view_story.html', {'selected_story':selected_story,'is_video':is_video,'user_stories':user_stories,'user':user})

def reels(request):
    return render(request,'reels.html')
