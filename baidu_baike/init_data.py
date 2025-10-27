import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baidu_baike.settings')
django.setup()

from encyclopedia.models import Article
from django.utils import timezone

def init_sample_data():
    """初始化示例数据"""
    print("正在初始化示例数据...")
    
    # 检查是否已有数据
    if Article.objects.exists():
        print("数据库中已有数据，跳过初始化")
        return
    
    # 创建示例词条
    sample_articles = [
        {
            'title': '人工智能',
            'content': '人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，它试图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。\n\n人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的“容器”。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。',
            'category': '科技',
        },
        {
            'title': '中国历史',
            'content': '中国历史是指中国从中华文明产生到现在的历史。中国历史悠久，自黄帝部落的姬轩辕（也称公孙轩辕）时期算起约有5000年；从三皇五帝算起约有4600年；自夏朝算起约有近4100年；从中国第一次大统一的中央集权制的秦朝算起约有2240年。\n\n中国历经多次政权演变和朝代更迭，也曾是世界上最强大的国家，经济、文化、科技世界瞩目。\n\n中国史前时期社会生产力发展，早期文化多元发展、互相渗透、融聚一体，炎黄被尊奉为中华民族的人文始祖。',
            'category': '历史',
        },
        {
            'title': '自然保护区',
            'content': '自然保护区是指对有代表性的自然生态系统、珍稀濒危野生动植物物种的天然集中分布区、有特殊意义的自然遗迹等保护对象所在的陆地、陆地水体或者海域，依法划出一定面积予以特殊保护和管理的区域。\n\n自然保护区是自然保护地的一种类型，主要保护具有生态代表性的自然区域和珍稀濒危野生动植物。中国的自然保护区分为国家级自然保护区和地方级自然保护区，其中地方级又包括省、市、县三级自然保护区。',
            'category': '自然',
        }
    ]
    
    for article_data in sample_articles:
        article = Article(**article_data)
        article.save()
        print(f"创建词条: {article.title}")
    
    print("示例数据初始化完成！")

if __name__ == '__main__':
    init_sample_data()