from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag
from .serializers import PostSerializer, CategorySerializer, TagSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author", "category").prefetch_related("tags").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "category__slug": ["exact"],
        "author__username": ["exact"],
        "is_published": ["exact"],
        "published_date": ["gte", "lte"],
        "tags__slug": ["exact"],
    }
    search_fields = ["title", "content", "tags__name", "author__username"]
    ordering_fields = ["published_date", "created_at", "category__name"]
    ordering = ["-published_date", "-created_at"]

    def perform_create(self, serializer):
        # ensure the author is the currently authenticated user
        user = self.request.user
        # If not authenticated, serializer's author field must be provided (but permission will block writes)
        if user and user.is_authenticated:
            serializer.save(author=user)
        else:
            # allow creating with author field if provided (for admin/testing)
            serializer.save()

    @action(detail=False, methods=["get"], url_path="by-author/(?P<username>[^/.]+)")
    def by_author(self, request, username=None):
        qs = self.filter_queryset(self.get_queryset().filter(author__username=username))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-category/(?P<slug>[^/.]+)")
    def by_category(self, request, slug=None):
        qs = self.filter_queryset(self.get_queryset().filter(category__slug=slug))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
