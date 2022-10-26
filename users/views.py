from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .serializers import CustomTokenObtainPairSerializer

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"가입 완료!!"}, status=status.HTTP_201_CREATED)
        return Response({"msg":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)



class CutomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer