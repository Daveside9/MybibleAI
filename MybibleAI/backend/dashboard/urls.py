
from django.urls import path
from .views import AdminStatsView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('stats', AdminStatsView.as_view(), name='admin-stats'),
    path('users', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>', AdminUserDetailView.as_view(), name='admin-user-detail'),
]
