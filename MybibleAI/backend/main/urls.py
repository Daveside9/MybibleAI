
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, CustomTokenObtainPairView, ChatViewSet, user_detail_view

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('auth/signup', SignupView.as_view(), name='signup'),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/me/', user_detail_view, name='user-detail'),
    path('', include(router.urls)),
]
