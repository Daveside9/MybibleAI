
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Chat, User
from .serializers import SignupSerializer, ChatSerializer, UserSerializer
# Custom Login View to match frontend's FormData
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    This custom serializer is needed because the frontend sends 'username'
    but our User model uses 'email' as the USERNAME_FIELD.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        # token['name'] = user.name
        return token

    def validate(self, attrs):
        # The default validation uses the USERNAME_FIELD to get the user.
        # Since the frontend sends 'username' (which is the email), this works out of the box.
        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    This view uses the default form parser, which handles FormData,
    and our custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to login

# Signup View
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to signup

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the chats
        for the currently authenticated user.
        """
        return self.request.user.chats.all()

    def perform_create(self, serializer):
        """
        Assign the current user to the chat.
        """
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail_view(request):
    """
    Retrieve the authenticated user's details.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
