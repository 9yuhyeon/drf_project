from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('mock/', views.MockView.as_view(), name='mock_view'),
    path('api/token/', views.CutomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
