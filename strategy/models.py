from django.db import models

from accounts.models import CustomUser

from django.utils import timezone

class Category(models.Model):

    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )


    def __str__(self):

        return self.title
    
    
class StrategyPost(models.Model):

    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',

        on_delete=models.PROTECT
    )


    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )

    comment1 = models.TextField(
        verbose_name='コメント1',
    )

    comment2 = models.TextField(
        verbose_name='コメント2',
        blank=True,
        null=True,
    )

    comment3 = models.TextField(
        verbose_name='コメント3',
        blank=True,
        null=True,

    )

    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to= 'photos'
    )

    image2 = models.ImageField(
        verbose_name='イメージ2',
        upload_to= 'photos',
        blank=True,
        null=True,

    )

    image3 = models.ImageField(
        verbose_name='イメージ3',
        upload_to= 'photos',
        blank=True,
        null=True,
    )

    posted_at = models.DateField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    def __str__(self):

        return self.title
    
class Comment(models.Model):
    """記事に紐づくコメント"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('本文')
    target = models.ForeignKey(StrategyPost, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)
 
    def __str__(self):
        return self.text[:20]
    
class LikeForPost(models.Model):
    """投稿に対するいいね"""
    target = models.ForeignKey(StrategyPost, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

class LikeForComment(models.Model):
    """コメントに対するいいね"""
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)