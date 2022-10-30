from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from articles.serializers import ArticleListSerializer
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    follow = serializers.StringRelatedField(many=True)
    follower = serializers.StringRelatedField(many=True)
    article_set = ArticleListSerializer(many=True)
    like_articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = ('id','email','follow','follower','article_set', 'like_articles') # 내 게시글, 좋아요 한 글 추가하기


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token