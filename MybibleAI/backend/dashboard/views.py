
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from main.models import User, Chat
from main.serializers import UserSerializer # Re-use the UserSerializer
from .permissions import IsAdminUser

# Create your views here.

class AdminStatsView(APIView):
    """
    Provides statistics for the admin dashboard.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_chats = Chat.objects.count()
        # NOTE: active_users logic would depend on your definition of "active"
        # For now, we'll just return total users.
        stats = {
            "total_users": total_users,
            "active_users": total_users, 
            "total_chats": total_chats,
        }
        return Response(stats)

class AdminUserListView(generics.ListCreateAPIView):
    """
    Allows admins to list and create users.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows admins to retrieve, update, and delete a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
