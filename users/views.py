from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from .serializers import UserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer



class CutomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"가입 완료!!"}, status=status.HTTP_201_CREATED)
        return Response({"msg":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializers = UserProfileSerializer(user)
        return Response(serializers.data, status=status.HTTP_200_OK)


class FollowView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        me = request.user
        if me in user.follower.all():
            user.follower.remove(me)
            return Response('팔로우 취소', status=status.HTTP_200_OK)
        else:
            user.follower.add(me)
            return Response('팔로우', status=status.HTTP_200_OK)


class MockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        # user.is_authenticated = True
        # user.save()
        return Response('GET 요청')