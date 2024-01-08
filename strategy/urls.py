from django.urls import path
from . import views

app_name = 'strategy'


urlpatterns = [

    # トップページ表示するためにviewsのトップページ用のやつを実行する。
    path('', views.IndexView.as_view(), name='index'),

    path('post/', views.CreateStrategyView.as_view(), name='post'),

    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),

    path('strategy-detail/<int:pk>',
         views.DetailView.as_view(),
         name = 'strategy_detail'
         ),

    path('strategy/<int:pk>/delete/',
         views.StrategyDeleteView.as_view(),
         name = 'strategy_delete'
         ),


    path('mypage/', views.MypageView.as_view(),
         name = 'mypage'),

    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'), 

    path('like_for_post/', views.like_for_post, name='like_for_post'), 

    path('contact/',views.ContactView.as_view(),name='contact'
        ),

]