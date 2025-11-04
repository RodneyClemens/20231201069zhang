import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baidu_baike.settings')
django.setup()

from django.contrib.auth.models import User
from encyclopedia.models import UserProfile, Category, Forum, Post, Comment, UserFollow, Like
from django.utils import timezone
import random

def init_sample_data():
    """初始化示例数据"""
    print("正在初始化示例数据...")
    
    # 检查是否已有数据
    if Forum.objects.exists():
        print("数据库中已有数据，跳过初始化")
        return
    
    # 创建分类
    print("创建分类...")
    categories = [
        {'name': '科技', 'description': '科技相关讨论', 'icon': 'fa-microchip'},
        {'name': '电影', 'description': '电影相关讨论', 'icon': 'fa-film'},
        {'name': '游戏', 'description': '游戏相关讨论', 'icon': 'fa-gamepad'},
        {'name': '音乐', 'description': '音乐相关讨论', 'icon': 'fa-music'},
        {'name': '体育', 'description': '体育相关讨论', 'icon': 'fa-futbol'},
        {'name': '生活', 'description': '生活相关讨论', 'icon': 'fa-home'},
        {'name': '学习', 'description': '学习相关讨论', 'icon': 'fa-book'},
    ]
    
    category_objects = []
    for cat_data in categories:
        cat = Category.objects.create(**cat_data)
        category_objects.append(cat)
        print(f"创建分类: {cat.name}")
    
    # 创建用户
    print("创建用户...")
    users = [
        {'username': '69', 'email': '69@example.com', 'password': '123456'},
        {'username': '张三', 'email': 'zhangsan@example.com', 'password': '123456'},
        {'username': '李四', 'email': 'lisi@example.com', 'password': '123456'},
        {'username': '王五', 'email': 'wangwu@example.com', 'password': '123456'},
    ]
    
    user_objects = []
    for user_data in users:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user_objects.append(user)
        
        # 创建用户扩展信息
        profile_data = {
            'bio': f'大家好，我是{user_data["username"]}，欢迎关注我！',
            'followers': random.randint(0, 100),
            'following': random.randint(0, 50),
        }
        
        # 为用户69设置特殊信息
        if user_data['username'] == '69':
            profile_data['bio'] = '我是69，热爱科技和游戏，乐于分享生活点滴！'
            profile_data['followers'] = 256
            profile_data['following'] = 42
            profile_data['avatar'] = 'https://randomuser.me/api/portraits/men/69.jpg'
        
        UserProfile.objects.create(user=user, **profile_data)
        print(f"创建用户: {user.username}")
    
    # 创建贴吧
    print("创建贴吧...")
    forums = [
        {
            'name': '科技前沿',
            'description': '讨论最新科技动态和前沿技术',
            'category': category_objects[0],
            'creator': user_objects[0],
            'members_count': random.randint(1000, 10000),
            'cover_image': 'https://picsum.photos/id/1/800/200'
        },
        {
            'name': '电影爱好者',
            'description': '分享电影心得和影评',
            'category': category_objects[1],
            'creator': user_objects[1],
            'members_count': random.randint(2000, 8000),
            'cover_image': 'https://picsum.photos/id/20/800/200'
        },
        {
            'name': '游戏世界',
            'description': '游戏攻略、新闻和讨论',
            'category': category_objects[2],
            'creator': user_objects[0],
            'members_count': random.randint(3000, 15000),
            'cover_image': 'https://picsum.photos/id/237/800/200'
        },
        {
            'name': '音乐分享',
            'description': '分享你喜欢的音乐',
            'category': category_objects[3],
            'creator': user_objects[2],
            'members_count': random.randint(1500, 7000),
            'cover_image': 'https://picsum.photos/id/1025/800/200'
        },
        {
            'name': '足球吧',
            'description': '足球赛事和球星讨论',
            'category': category_objects[4],
            'creator': user_objects[3],
            'members_count': random.randint(5000, 20000),
            'cover_image': 'https://picsum.photos/id/1060/800/200'
        },
    ]
    
    forum_objects = []
    for forum_data in forums:
        forum = Forum.objects.create(**forum_data)
        forum_objects.append(forum)
        
        # 让创建者关注自己的贴吧
        UserFollow.objects.create(user=forum.creator, forum=forum)
        
        print(f"创建贴吧: {forum.name}")
    
    # 创建帖子
    print("创建帖子...")
    posts_data = [
        {
            'forum': forum_objects[0],
            'title': '人工智能的未来发展趋势',
            'content': '人工智能技术正在飞速发展，未来将会在医疗、教育、交通等多个领域带来革命性变化。特别是大语言模型的出现，让AI在理解和生成人类语言方面取得了巨大进步。\n\n![AI图片](https://picsum.photos/id/180/600/400)\n\n大家觉得AI会在哪些领域最先改变我们的生活？',
            'author': user_objects[0],
            'is_top': True,
            'views_count': random.randint(1000, 5000)
        },
        {
            'forum': forum_objects[1],
            'title': '流浪地球3即将上映，你期待吗？',
            'content': '据官方消息，流浪地球3已经进入后期制作阶段，预计明年春节档上映。前两部都取得了巨大成功，第三部会带来怎样的惊喜呢？\n\n![电影海报](https://picsum.photos/id/201/600/400)\n\n你最期待第三部中看到哪些情节或角色？',
            'author': user_objects[1],
            'is_top': False,
            'views_count': random.randint(2000, 8000)
        },
        {
            'forum': forum_objects[2],
            'title': '原神新版本攻略分享',
            'content': '新版本更新了很多内容，这里给大家分享一些实用的攻略和技巧。\n\n1. 新角色培养建议\n2. 副本攻略\n3. 隐藏任务触发条件\n\n![游戏截图](https://picsum.photos/id/235/600/400)\n\n欢迎大家在评论区补充！',
            'author': user_objects[0],
            'is_top': True,
            'views_count': random.randint(5000, 15000)
        },
        {
            'forum': forum_objects[3],
            'title': '最近发现的宝藏音乐推荐',
            'content': '最近听到了一些非常好听的歌曲，想和大家分享一下。这些歌曲可能比较小众，但真的很有特色。\n\n1. 《星空》- 未知歌手\n2. 《晚风》- 独立音乐人\n3. 《城市之光》- 新晋乐队\n\n希望大家喜欢这些音乐推荐！',
            'author': user_objects[2],
            'is_top': False,
            'views_count': random.randint(800, 3000)
        },
        {
            'forum': forum_objects[4],
            'title': '世界杯预选赛：中国VS韩国前瞻',
            'content': '这场比赛将于下周二晚上进行，中国队需要全力争取积分。虽然实力上有差距，但相信队员们会拼尽全力。\n\n![足球比赛](https://picsum.photos/id/433/600/400)\n\n大家预测一下比分会是多少？',
            'author': user_objects[3],
            'is_top': False,
            'views_count': random.randint(3000, 10000)
        },
    ]
    
    post_objects = []
    for post_data in posts_data:
        post = Post.objects.create(**post_data)
        post_objects.append(post)
        
        # 更新贴吧帖子数
        post.forum.posts_count += 1
        post.forum.save()
        
        # 更新用户发帖数
        post.author.profile.posts_count += 1
        post.author.profile.save()
        
        print(f"创建帖子: {post.title}")
    
    # 创建评论
    print("创建评论...")
    comments_data = [
        {
            'post': post_objects[0],
            'author': user_objects[1],
            'content': '我觉得AI在医疗领域的应用会最先成熟，特别是在疾病诊断方面。'
        },
        {
            'post': post_objects[0],
            'author': user_objects[2],
            'content': '教育领域也很有潜力，个性化学习将成为可能。'
        },
        {
            'post': post_objects[1],
            'author': user_objects[0],
            'content': '非常期待！前两部的特效真的很震撼。'
        },
        {
            'post': post_objects[1],
            'author': user_objects[3],
            'content': '希望故事情节能更加紧凑一些。'
        },
        {
            'post': post_objects[2],
            'author': user_objects[1],
            'content': '感谢分享！新角色的培养材料在哪里刷比较快？'
        },
        {
            'post': post_objects[2],
            'author': user_objects[0],
            'content': '回复：在新开放的地图区域，每天有概率刷新。'
        },
    ]
    
    comment_objects = []
    for comment_data in comments_data:
        # 为部分评论设置父评论，模拟回复
        if comment_data['post'] == post_objects[2] and comment_data['author'] == user_objects[0]:
            comment_data['parent'] = comment_objects[4]  # 回复第五个评论
        
        comment = Comment.objects.create(**comment_data)
        comment_objects.append(comment)
        
        # 更新帖子评论数
        comment.post.comments_count += 1
        comment.post.save()
        
        print(f"创建评论: {comment.author.username} 评论了 {comment.post.title}")
    
    # 模拟点赞
    print("模拟点赞...")
    for post in post_objects:
        likes_count = random.randint(10, 100)
        post.likes_count = likes_count
        post.save()
        
        # 随机让一些用户点赞
        for user in random.sample(user_objects, min(likes_count // 10, len(user_objects))):
            Like.objects.create(user=user, content_type='post', content_id=post.id)
    
    for comment in comment_objects:
        likes_count = random.randint(0, 20)
        comment.likes_count = likes_count
        comment.save()
    
    print("示例数据初始化完成！")

if __name__ == '__main__':
    init_sample_data()