from rest_framework import serializers
from .models import Article, Comment


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
        
    class Meta:
        model = Comment
        exclude = ('article',)


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    likes = serializers.StringRelatedField(many=True)
    
    def get_user(self, obj):
        return obj.user.email
        
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','content','image')


class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = ('id','title','image','created_at','user','likes','comments')
