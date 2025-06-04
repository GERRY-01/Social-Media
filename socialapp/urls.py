from django.urls import path
from . import views

urlpatterns = [
    path('/home', views.home, name="home"),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('likes/<int:post_id>', views.likes, name="likes"),
    path('/profile',views.profile,name="profile"),
]
