from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateUpdateView, ArticleSearchAPI

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('create/', ArticleCreateUpdateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleCreateUpdateView.as_view(), name='article_edit'),
    path('api/search/', ArticleSearchAPI.as_view(), name='article_search_api'),
]