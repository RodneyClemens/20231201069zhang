from django.urls import path
from .views import (
    index, category_list, forum_detail, post_detail,
    user_login, user_register, user_logout, user_profile,
    create_post, add_comment, toggle_follow, toggle_like, search
)

urlpatterns = [
    # 首页和分类
    path('', index, name='index'),
    path('categories/', category_list, name='categories'),
    path('categories/<int:category_id>/', category_list, name='category_detail'),
    
    # 贴吧相关
    path('forum/<int:forum_id>/', forum_detail, name='forum_detail'),
    path('forum/<int:forum_id>/create-post/', create_post, name='create_post'),
    path('forum/<int:forum_id>/follow/', toggle_follow, name='toggle_follow'),
    
    # 帖子相关
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('like/<str:content_type>/<int:content_id>/', toggle_like, name='toggle_like'),
    
    # 用户相关
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    
    # 搜索
    path('search/', search, name='search'),
]