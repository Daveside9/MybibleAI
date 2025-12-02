
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    # The 'name' field from your signup form
    name = models.CharField(max_length=255)
    
    # Use email as the unique identifier for login
    email = models.EmailField(unique=True)
    
    # We don't need a separate username, so let's use email for that.
    # The 'username' field from AbstractUser will now store the email.
    USERNAME_FIELD = 'email'
    
    # 'username' is required by default, but we are using email,
    # so we need to remove it from the required fields list.
    # 'name' is also added here as it's a required field on our form.
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Chat(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.deletion.CASCADE,
        related_name="chats"
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Chat with {self.user.username} - {self.title}"
