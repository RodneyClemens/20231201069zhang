from django.db import models
from django.utils import timezone


class Article(models.Model):
    """百科词条模型"""
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='词条标题'
    )
    content = models.TextField(
        verbose_name='词条内容'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='词条分类'
    )
    create_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='创建时间'
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='最后修改时间'
    )

    class Meta:
        verbose_name = '百科词条'
        verbose_name_plural = '百科词条'
        ordering = ['-update_time']

    def __str__(self):
        return self.title