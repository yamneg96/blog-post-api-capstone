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
        """
        Assign the currently authenticated user as the author.
        If no user is authenticated, use a default user (first user in DB).
        """
        user = self.request.user
        if user.is_anonymous:
            # Get the first user in the database as default (ensure at least one user exists)
            user = User.objects.first()
            if not user:
                # If no user exists, raise an error
                raise ValueError("No users exist in the database. Create a user first.")
        serializer.save(author=user)

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
