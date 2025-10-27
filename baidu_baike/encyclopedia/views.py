from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Article
from django.views import View
from django.http import JsonResponse
import json


class ArticleListView(View):
    """词条列表页视图"""
    def get(self, request):
        articles = Article.objects.all()
        categories = list(Article.objects.values_list('category', flat=True).distinct())
        categories_json = json.dumps(categories)
        return render(request, 'encyclopedia/article_list.html', {
            'articles': articles,
            'categories': categories_json
        })


class ArticleDetailView(View):
    """词条详情页视图"""
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'encyclopedia/article_detail.html', {'article': article})


class ArticleCreateUpdateView(View):
    """创建/编辑词条视图"""
    def get(self, request, pk=None):
        if pk:
            article = get_object_or_404(Article, pk=pk)
        else:
            article = None
        return render(request, 'encyclopedia/article_form.html', {'article': article})

    def post(self, request, pk=None):
        data = request.POST
        if pk:
            article = get_object_or_404(Article, pk=pk)
            article.title = data.get('title')
            article.content = data.get('content')
            article.category = data.get('category')
            article.save()
        else:
            article = Article.objects.create(
                title=data.get('title'),
                content=data.get('content'),
                category=data.get('category')
            )
        return redirect(reverse('article_detail', kwargs={'pk': article.pk}))


class ArticleSearchAPI(View):
    """词条搜索API，用于Vue.js交互"""
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        category = request.GET.get('category', '')
        
        articles = Article.objects.all()
        
        if keyword:
            articles = articles.filter(title__icontains=keyword)
        if category:
            articles = articles.filter(category=category)
        
        results = [{
            'id': article.pk,
            'title': article.title,
            'category': article.category,
            'update_time': article.update_time.strftime('%Y-%m-%d %H:%M:%S')
        } for article in articles]
        
        return JsonResponse({'articles': results})