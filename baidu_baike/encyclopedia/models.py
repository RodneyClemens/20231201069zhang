from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=255, default='https://randomuser.me/api/portraits/men/32.jpg', verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    followers = models.IntegerField(default=0, verbose_name='粉丝数')
    following = models.IntegerField(default=0, verbose_name='关注数')
    posts_count = models.IntegerField(default=0, verbose_name='发帖数')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return self.user.username


class Category(models.Model):
    """贴吧分类"""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    icon = models.CharField(max_length=50, default='fa-tag', verbose_name='分类图标')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
    
    def __str__(self):
        return self.name


class Forum(models.Model):
    """贴吧模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='贴吧名称')
    description = models.TextField(blank=True, verbose_name='贴吧描述')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums', verbose_name='所属分类')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    members_count = models.IntegerField(default=0, verbose_name='成员数')
    posts_count = models.IntegerField(default=0, verbose_name='帖子数')
    cover_image = models.CharField(max_length=255, default='https://picsum.photos/800/200', verbose_name='封面图')
    
    class Meta:
        verbose_name = '贴吧'
        verbose_name_plural = '贴吧'
        ordering = ['-members_count']
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """帖子模型"""
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts', verbose_name='所属贴吧')
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    views_count = models.IntegerField(default=0, verbose_name='浏览量')
    likes_count = models.IntegerField(default=0, verbose_name='点赞数')
    comments_count = models.IntegerField(default=0, verbose_name='评论数')
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    is_精华 = models.BooleanField(default=False, verbose_name='精华')
    
    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-is_top', '-create_time']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """评论模型"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='所属帖子')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='评论时间')
    likes_count = models.IntegerField(default=0, verbose_name='点赞数')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['create_time']
    
    def __str__(self):
        return f'{self.author.username} 评论了 {self.post.title}'


class UserFollow(models.Model):
    """用户关注贴吧关系"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='followers')
    create_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'forum')
        verbose_name = '用户关注'
        verbose_name_plural = '用户关注'
    
    def __str__(self):
        return f'{self.user.username} 关注了 {self.forum.name}'


class Like(models.Model):
    """点赞模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.CharField(max_length=20, choices=[('post', '帖子'), ('comment', '评论')])
    content_id = models.IntegerField()
    create_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'content_type', 'content_id')
        verbose_name = '点赞'
        verbose_name_plural = '点赞'