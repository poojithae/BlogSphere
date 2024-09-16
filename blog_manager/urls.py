from django.urls import path
from .views import (
    BlogPostListCreateView, 
    BlogPostDetailView, 
    CommentListCreateView, 
    CommentDetailView, 
    CategoryListView, 
    TagListView, 
    ReactionListCreateView, 
    ReactionDetailView, 
    UserProfileView, 
    RegisterView,
    SearchView 
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('blogposts/', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('blogposts/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list-create'),
    path('tags/', TagListView.as_view(), name='tag-list-create'),
    path('reactions/', ReactionListCreateView.as_view(), name='reaction-list-create'),
    path('reactions/<int:pk>/', ReactionDetailView.as_view(), name='reaction-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('search/', SearchView.as_view(), name='search'),
    
]
