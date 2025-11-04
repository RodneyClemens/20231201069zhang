from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Category, Forum, Post, Comment, UserFollow, Like
import json


def index(request):
    """首页视图"""
    # 获取热门贴吧
    hot_forums = Forum.objects.all().order_by('-members_count')[:10]
    
    # 获取最新帖子
    latest_posts = Post.objects.all().order_by('-create_time')[:20]
    
    # 获取热门帖子
    hot_posts = Post.objects.all().order_by('-views_count')[:10]
    
    # 获取所有分类
    categories = Category.objects.all()
    
    context = {
        'hot_forums': hot_forums,
        'latest_posts': latest_posts,
        'hot_posts': hot_posts,
        'categories': categories,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/index.html', context)


def category_list(request, category_id=None):
    """分类列表视图"""
    categories = Category.objects.all()
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        forums = Forum.objects.filter(category=category).order_by('-members_count')
    else:
        category = None
        forums = Forum.objects.all().order_by('-members_count')
    
    context = {
        'categories': categories,
        'current_category': category,
        'forums': forums,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/category_list.html', context)


def forum_detail(request, forum_id):
    """贴吧详情视图"""
    forum = get_object_or_404(Forum, id=forum_id)
    
    # 获取帖子列表，可以根据参数排序
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'hot':
        posts = forum.posts.filter().order_by('-views_count')
    elif sort_by == 'comments':
        posts = forum.posts.filter().order_by('-comments_count')
    else:
        posts = forum.posts.filter().order_by('-is_top', '-create_time')
    
    # 检查用户是否已关注
    is_following = False
    if request.user.is_authenticated:
        is_following = UserFollow.objects.filter(user=request.user, forum=forum).exists()
    
    context = {
        'forum': forum,
        'posts': posts,
        'is_following': is_following,
        'sort_by': sort_by,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/forum_detail.html', context)


def post_detail(request, post_id):
    """帖子详情视图"""
    post = get_object_or_404(Post, id=post_id)
    
    # 增加浏览量
    post.views_count += 1
    post.save()
    
    # 获取评论列表（只获取顶级评论）
    comments = Comment.objects.filter(post=post, parent=None).order_by('create_time')
    
    # 检查用户是否已点赞
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, content_type='post', content_id=post.id).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/post_detail.html', context)


def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'message': '登录成功'})
        else:
            return JsonResponse({'success': False, 'message': '用户名或密码错误'})
    
    return render(request, 'encyclopedia/login.html')


def user_register(request):
    """用户注册视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': '用户名已存在'})
        
        # 创建用户
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # 创建用户扩展信息
        UserProfile.objects.create(user=user)
        
        # 自动登录
        login(request, user)
        
        return JsonResponse({'success': True, 'message': '注册成功'})
    
    return render(request, 'encyclopedia/register.html')


def user_logout(request):
    """用户登出视图"""
    logout(request)
    return redirect('index')


def user_profile(request, username):
    """用户个人中心"""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    
    # 获取用户的帖子
    user_posts = Post.objects.filter(author=user).order_by('-create_time')
    
    # 获取用户关注的贴吧
    followed_forums = []
    if request.user.is_authenticated:
        followed_forums = Forum.objects.filter(followers__user=request.user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_posts': user_posts,
        'followed_forums': followed_forums,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/user_profile.html', context)


@login_required
def create_post(request, forum_id):
    """创建帖子视图"""
    forum = get_object_or_404(Forum, id=forum_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if not title or not content:
            return JsonResponse({'success': False, 'message': '标题和内容不能为空'})
        
        # 创建帖子
        post = Post.objects.create(
            forum=forum,
            title=title,
            content=content,
            author=request.user
        )
        
        # 更新贴吧帖子数
        forum.posts_count += 1
        forum.save()
        
        # 更新用户发帖数
        profile = request.user.profile
        profile.posts_count += 1
        profile.save()
        
        return JsonResponse({'success': True, 'message': '帖子发布成功', 'post_id': post.id})
    
    context = {
        'forum': forum,
        'current_user': request.user
    }
    
    return render(request, 'encyclopedia/create_post.html', context)


@login_required
def add_comment(request, post_id):
    """添加评论视图"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if not content:
            return JsonResponse({'success': False, 'message': '评论内容不能为空'})
        
        comment_data = {
            'post': post,
            'author': request.user,
            'content': content
        }
        
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
            comment_data['parent'] = parent
        
        # 创建评论
        comment = Comment.objects.create(**comment_data)
        
        # 更新帖子评论数
        post.comments_count += 1
        post.save()
        
        return JsonResponse({'success': True, 'message': '评论成功'})
    
    return JsonResponse({'success': False, 'message': '请求方法错误'})


@login_required
def toggle_follow(request, forum_id):
    """关注/取消关注贴吧"""
    forum = get_object_or_404(Forum, id=forum_id)
    
    follow, created = UserFollow.objects.get_or_create(user=request.user, forum=forum)
    
    if created:
        # 关注
        forum.members_count += 1
        forum.save()
        request.user.profile.following += 1
        request.user.profile.save()
        return JsonResponse({'success': True, 'message': '关注成功', 'is_following': True})
    else:
        # 取消关注
        follow.delete()
        forum.members_count = max(0, forum.members_count - 1)
        forum.save()
        request.user.profile.following = max(0, request.user.profile.following - 1)
        request.user.profile.save()
        return JsonResponse({'success': True, 'message': '取消关注成功', 'is_following': False})


@login_required
def toggle_like(request, content_type, content_id):
    """点赞/取消点赞"""
    if content_type not in ['post', 'comment']:
        return JsonResponse({'success': False, 'message': '不支持的内容类型'})
    
    # 验证内容是否存在
    if content_type == 'post':
        content = get_object_or_404(Post, id=content_id)
    else:
        content = get_object_or_404(Comment, id=content_id)
    
    like, created = Like.objects.get_or_create(user=request.user, content_type=content_type, content_id=content_id)
    
    if created:
        # 点赞
        content.likes_count += 1
        content.save()
        return JsonResponse({'success': True, 'message': '点赞成功', 'is_liked': True, 'likes_count': content.likes_count})
    else:
        # 取消点赞
        like.delete()
        content.likes_count = max(0, content.likes_count - 1)
        content.save()
        return JsonResponse({'success': True, 'message': '取消点赞成功', 'is_liked': False, 'likes_count': content.likes_count})


def search(request):
    """搜索功能"""
    keyword = request.GET.get('keyword', '')
    
    if keyword:
        # 搜索帖子
        posts = Post.objects.filter(title__icontains=keyword) | Post.objects.filter(content__icontains=keyword)
        
        # 搜索贴吧
        forums = Forum.objects.filter(name__icontains=keyword) | Forum.objects.filter(description__icontains=keyword)
        
        # 搜索用户
        users = User.objects.filter(username__icontains=keyword)
    else:
        posts = []
        forums = []
        users = []
    
    context = {
        'keyword': keyword,
        'posts': posts,
        'forums': forums,
        'users': users,
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'encyclopedia/search_results.html', context)