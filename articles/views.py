import re
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer
from articles import serializers

# Create your views here.
class ArticleView(APIView):
    def get(self, request): # 게시글 전체 모아보기(메인 page)
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request): # 게시글 작성 API
        serializers = ArticleCreateSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, article_id): # 특정 게시글 상세 페이지
        article = get_object_or_404(Article, id=article_id)
        serializers = ArticleSerializer(article)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def put(self, request, article_id): # 특정 게시글 수정
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializers = ArticleCreateSerializer(article, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"다른 사람의 게시글은 수정할 수 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id): # 특정 게시글 삭제
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response({"msg":"삭제되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"다른 사람의 게시글은 삭제할 수 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    def get(self, request, article_id): # 특정 게시글의 댓글 보기
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, article_id): # 특정 게시글의 댓글 작성
        serializers = CommentCreateSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user, article_id=article_id)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id): # 특정 게시물의 특정 댓글 수정
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            serializers = CommentCreateSerializer(comment, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("다른 사람의 댓글은 수정할 수 없습니다!", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self,request, article_id, comment_id): # 특정 게시물의 특정 댓글 삭제
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response('삭제 완료!', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('다른 사람의 댓글은 삭제할 수 없습니다!', status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요 취소!", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요!", status=status.HTTP_200_OK)