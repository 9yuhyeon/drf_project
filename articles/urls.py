from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'), # 메인(게시글 모아보기, 게시글 작성)
    path('feed/', views.FeedView.as_view(), name='feed_view'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'), # 게시글 상세 페이지(보기, 수정, 삭제)
    path('<int:article_id>/comment/', views.CommentView.as_view(), name='comment_view'), # 특정 게시글의 댓글(보기, 작성)
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'), # 특정 게시글의 특정 댓글(수정, 삭제)
    path('<int:article_id>/like/', views.LikeView.as_view(), name='like_view'),
]