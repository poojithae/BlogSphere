from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.response import Response
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
from blog_manager import permissions
from .permissions import IsAdminUser, IsAuthorOrAdmin, IsRegularUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.throttling import ScopedRateThrottle

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class BlogPostPagination(PageNumberPagination):
    page_size = 10

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = BlogPostFilter
    ordering_fields = ['created_at', 'title']
    ordering = ['created_at']
    throttle_scope = 'blog_categories'
    throttle_classes = [ScopedRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}_blog_post_list"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)
        response = super().get(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=CACHE_TTL)
        return response

    def perform_create(self, serializer):
        blog_post = serializer.save()
        cache.delete(f"{settings.KEY_PREFIX}_blog_post_list")

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'blog_categories'
    throttle_classes = [ScopedRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}_blog_post_detail_{kwargs['pk']}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)
        response = super().get(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=CACHE_TTL)
        return response
        
    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache_key = f"{settings.KEY_PREFIX}_blog_post_detail_{self.kwargs['pk']}"
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache_key = f"{settings.KEY_PREFIX}_blog_post_detail_{self.kwargs['pk']}"
        cache.delete(cache_key)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] 

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  

class ReactionListCreateView(generics.ListCreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRegularUser() if not self.request.user.is_staff else IsAdminUser()]
        return [AllowAny()]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            post = serializer.validated_data['post']
            if post.author != self.request.user:
                raise permissions.PermissionDenied("You do not have permission to react to this post.")
        serializer.save(user=self.request.user)
        cache.delete(f"{settings.KEY_PREFIX}reaction_list")

class ReactionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsRegularUser() if not self.request.user.is_staff else IsAdminUser()]
        return [AllowAny()]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

import logging
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View

# Configure your loggers
logger_info = logging.getLogger('django')
logger_city = logging.getLogger('city_log')

class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger_info.info('Login attempt for user: %s', username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger_info.info('User %s logged in successfully.', username)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            logger_city.error('Login failed for user: %s', username)
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        cache_key = f"{settings.KEY_PREFIX}_user_profile_{self.request.user.id}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if UserProfile.objects.filter(user=self.request.user).exists():
            return Response({"detail": "User profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save(user=request.user)
        cache_key = f"{settings.KEY_PREFIX}_user_profile_{self.request.user.id}"
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        cache.delete(f"{settings.KEY_PREFIX}_user_profile_{self.request.user.id}")
        return Response(serializer.data)
