from django.urls import path
from . import views

urlpatterns = [
    path('/home', views.home, name="home"),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('likes/<int:post_id>', views.likes, name="likes"),
    path('/profile',views.profile,name="profile"),
    path('follow/<int:user_id>',views.follow,name="follow"),
    path('view_profile/<int:user_id>',views.view_profile,name="view_profile"),
    path('/messages',views.messages,name="messages"),
    path('/view_story/<int:story_id>',views.view_story,name="view_story"),
    path('/reels',views.reels,name="reels"),
]
