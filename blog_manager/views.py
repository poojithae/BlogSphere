from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost, Comment, Category, Tag, Reaction, UserProfile
from .serializers import (
    BlogPostSerializer, 
    CommentSerializer, 
    CategorySerializer, 
    TagSerializer, 
    ReactionSerializer, 
    UserProfileSerializer,
    RegisterSerializer

)
from .filters import BlogPostFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
#from rest_framework.authentication import BaseAuthentication
from blog_manager import permissions
from .permissions import IsAdminUser, IsAuthorOrAdmin, IsRegularUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .tasks import cache_blog_post, cache_user_profile
from rest_framework.throttling import ScopedRateThrottle

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def get_blog_posts():
    print("DATA COMING FROM DB")
    return BlogPost.objects.all()

class BlogPostPagination(PageNumberPagination):
    page_size = 10
    # page_size_query_param = 'blog_page'
    # max_page_size = 100

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPagination
    #authentication_classes = [BaseAuthentication,]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = BlogPostFilter
    ordering_fields = ['created_at', 'title']
    ordering = ['created_at']
    throttle_scope = 'blog_categories'
    throttle_classes = [ScopedRateThrottle,]

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}_blog_post_list"
        print(f"Checking cache for key: {cache_key}")

        cached_response = cache.get(cache_key)
        if cached_response:
            print("DATA COMING FROM CACHE")
            return Response(cached_response)
        else:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=CACHE_TTL)
            print("DATA COMING FROM DB")
            return response
        
    def perform_create(self, serializer):
        blog_post = serializer.save()
        cache_blog_post.delay(blog_post.id)


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'blog_categories'
    throttle_classes = [ScopedRateThrottle,]

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}_blog_post_detail_{kwargs['pk']}"
        print(f"Checking cache for key: {cache_key}")

        cached_response = cache.get(cache_key)
        if cached_response:
            print("DATA COMING FROM CACHE")
            return Response(cached_response)
        else:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=CACHE_TTL)
            print("DATA COMING FROM DB")
            return response
        


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ReactionListCreateView(generics.ListCreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRegularUser() if not self.request.user.is_staff else IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            post = serializer.validated_data['post']
            if post.author != self.request.user:
                raise permissions.PermissionDenied("You do not have permission to react to this post.")
        serializer.save(user=self.request.user)

        cache_key = f"{settings.KEY_PREFIX}reaction_list"
        cache.delete(cache_key)
        print(f"Cache invalidated for key: {cache_key}")



class ReactionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsRegularUser() if not self.request.user.is_staff else IsAdminUser()]
        return [permissions.AllowAny()]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
    

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
             return None

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}user_profile_{self.request.user.id}"
        print(f"Checking cache for key: {cache_key}")

        cached_response = cache.get(cache_key)
        if cached_response:
            print("DATA COMING FROM CACHE")
            return Response(cached_response)
        else:
            print("DATA COMING FROM DB")
            user_profile = self.get_object()
            if user_profile is None:
                return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(user_profile)
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}user_profile_{self.request.user.id}"
        print(f"Checking cache for key: {cache_key}")

        user_profile = self.get_object()
        if user_profile is None:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

